import json
import os.path
import re
import time
import xml.etree.ElementTree as ET
from enum import Enum

import requests
import spacy
import speech_recognition as sr
import yake
from bs4 import BeautifulSoup
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from py3pin.Pinterest import Pinterest
from translate import Translator

translator = Translator(from_lang="it", to_lang='en')


class Language(Enum):
    ITALIANO = 1
    ENGLISH = 2


# si definisce la lingua iniziale
lang = Language.ITALIANO


def is_english():
    if lang == Language.ENGLISH:
        return True
    return False


def vocal_command_control(text):
    global lang
    comando_cambio_lingua = "cambio lingua inglese"
    command_change_language = "change language italian"
    if is_english():
        if text == command_change_language:
            lang = Language.ITALIANO
            print("LINGUA: ITALIANO")
    else:
        if text == comando_cambio_lingua:
            lang = Language.ENGLISH
            print("LINGUA: INGLESE")


app = Flask(__name__)

socketio = SocketIO(app, cors_allowed_origins='*')

pinterest = Pinterest(email="startupgarage@supsi.ch", password="pinGarageSG177", username="startupgarage0118")
pinterest.login()

text_global = ""
logs_json = {}
i = 0
seconds = 10
all_texts = []
all_images = []
all_times = []
all_links_img = []
all_links_patent = []
all_links_scholar = []
current_image = 0
background = "wood.png"
backgrounds = ["wood.png", "white.png", "black.png"]


# Search keyword
def search(keyword):
    search_batch = pinterest.search(scope='pins', query=keyword)

    # print(search_batch[0]) il primo è un profilo di pinterest inerente alla parola cercata
    # print(search_batch[1]["images"]["736x"]["url"]) stampa l'url dell'immagine
    # print(search_batch[1]["is_promoted"]) True sono le pubblicità, sponsorizzati da ..

    image_url = []
    image_link = []
    image_videos = []  # TODO da valutare se toglierlo

    for pins in search_batch:
        if "images" in pins.keys() and pins["is_promoted"] is False and len(image_url) < 5:
            image_url.append(pins["images"]["736x"]["url"])
            if pins["link"] is None:
                image_link.append("")
            else:
                image_link.append(pins["link"])
            if pins["videos"] is not None:
                image_videos.append(pins["videos"]["video_list"]["V_HLSV4"]["url"])

    data = {
        "all_data": {
            "word": keyword,
            "urls": image_url,
            "links": image_link,
            "urls_videos": image_videos
        }
    }
    return data


def search_patent(keyword):
    if is_english() is False:
        result = translator.translate(keyword)
        keyword = result

    # request access token
    header_access = {
        'Authorization': 'Basic QVJLOWdVYnVLWUQzaEpsbU9lRmdmRm94cXRNNXRyRkc6S1Q0dHhpc0F3VkpFOUVmOA==',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    param = {'grant_type': 'client_credentials'}

    url_access = 'https://ops.epo.org/3.2/auth/accesstoken'
    info = requests.post(url_access, headers=header_access, data=param)
    data_access = json.loads(info.text)  # data_access['access_token'] is the authorization
    auth = data_access['access_token']

    # search publication data
    url = 'http://ops.epo.org/3.2/rest-services/published-data/search?Range=1-5&q=ti%3D' + keyword
    header = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip',
        'Accept-Language': 'it-IT',
        'Authorization': 'Bearer ' + auth,
        'Host': 'ops.epo.org',
        'sec-ch-ua': 'Chromium";v="104',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': 'Windows',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML',
        'X-Forwarded-Port': '443',
        'X-Forwarded-Proto': 'https',
    }

    data = requests.get(url, headers=header)

    link_espacenet = []

    root = ET.fromstring(data.text)
    for elem in root.iter("{http://ops.epo.org}publication-reference"):
        family_id = elem.attrib["family-id"]
        country = elem.find("./{http://www.epo.org/exchange}document-id/{http://www.epo.org/exchange}country").text
        doc_number = elem.find(
            "./{http://www.epo.org/exchange}document-id/{http://www.epo.org/exchange}doc-number").text
        kind = elem.find("./{http://www.epo.org/exchange}document-id/{http://www.epo.org/exchange}kind").text
        doc_id = country + doc_number + kind
        link = "https://worldwide.espacenet.com/patent/search/family/" + family_id + "/publication/" + doc_id + "?q=" + doc_id
        # link_espacenet.append(link)
        doc_id2 = country + doc_number + "." + kind
        url2 = "http://ops.epo.org/3.2/rest-services/published-data/publication/epodoc/" + doc_id2 + "/biblio"
        data2 = requests.get(url2, headers=header)
        root2 = ET.fromstring(data2.text)
        title = root2.find(
            "./{http://www.epo.org/exchange}exchange-documents/{http://www.epo.org/exchange}exchange-document/{http://www.epo.org/exchange}bibliographic-data/{http://www.epo.org/exchange}invention-title")
        if title is not None:
            link_espacenet.append(title.text)
            link_espacenet.append(link)
    return link_espacenet


def search_scholar(keyword):
    url = 'https://scholar.google.com/scholar?hl=it&q=allintitle%3A+' + keyword
    data = requests.get(url)

    link_scholar = []

    html = BeautifulSoup(data.text, 'html.parser')
    results = html.select('.gs_r')

    for result in results:
        link = result.select('.gs_or_ggsm')
        if len(link) > 0:
            link = re.search('href=\"(.+?)\">', str(link[0].find('a'))).group(1)
            link_scholar.append(link)

    return link_scholar


# inizializzazione delle variabili necessarie per utilizzare le librerie per il filtro
kw_extractor = yake.KeywordExtractor()
nlp_it = spacy.load("en_core_web_trf")
nlp_en = spacy.load("it_core_news_lg")


def keyword_founder(audio_string):
    # inizializzazione delle variabili necessarie per utilizzare le librerie per il filtro
    if is_english():
        nlp = nlp_en
    else:
        nlp = nlp_it
    if is_english():
        language = "en"
    else:
        language = "it"
    max_ngram_size = 2  # numero massimo di parole per una parola chiave
    deduplication_threshold = 0.5  # una soglia di duplicazione delle parole nelle parole chiave trovate
    numOfKeywords = 50  # numero massimo di parole chiave trovabili
    custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_threshold,
                                                top=numOfKeywords, features=None)
    keywords_and_score = custom_kw_extractor.extract_keywords(audio_string)

    # copia delle parole chiave trovate dalla libreria in una lista
    keywords = []
    for kw in keywords_and_score:
        keywords.append(kw[0])
    # copia delle parole chiave trovate dalla libreria in un'altra lista
    keywords2 = []
    for kw in keywords_and_score:
        keywords2.append(kw[0])

    doc = nlp(audio_string)
    # analisi delle parole chiave trovate
    for word in keywords:
        single_word = nlp(word)
        if len(single_word) == 1:
            # ci si riferisce alle parole chiave composte da una parola
            for token in doc:
                if token.text == word and token.pos_ != "NOUN":
                    if word in keywords2:
                        keywords2.remove(word)
        else:
            # ci si riferisce alle parole chiave composte da due parole
            for token in doc:
                # print(token.text + " " + token.pos_)
                if token.text == single_word[0].text and \
                        (token.pos_ != 'NOUN' or token.pos_ != 'ADJ'):
                    keywords2.remove(word)
                    break
                elif token.text == single_word[1].text and \
                        (token.pos_ != 'NOUN' or token.pos_ != 'ADJ'):
                    keywords2.remove(word)
                    break
                elif token.text == single_word[0].text and (token.pos_ == 'DET' or token.pos_ == 'ADP'):
                    keywords.append(single_word[1].text)
                    keywords2.append(single_word[1].text)
                    keywords2.remove(word)
                    break

    if not is_english():
        if "stocazzo" in keywords2:
            keywords2.remove("stocazzo")
        if "coglioni" in keywords2:
            keywords2.remove("coglioni")
        if "ecc" in keywords2:
            keywords2.remove("ecc")
        if "fallo" in keywords2:
            keywords2.remove("fallo")
        if "falla" in keywords2:
            keywords2.remove("falla")

    if len(keywords2) > 0:
        return keywords2[-1]
    return []


r = sr.Recognizer()
mic = sr.Microphone(device_index=1)


# index.html con sfondo
@app.route('/')
def index():
    global background
    return render_template('index.html', background_value="../static/image_background/" + background)


# pagina settings
@app.route('/settings')
def settings():
    return render_template('settings.html')


# richiesta per impostare secondi
@app.route('/settings_seconds')
def settings_seconds():
    global seconds
    # prendo secondi
    seconds = request.args.get('seconds', 10, int)
    return render_template('settings.html')


# richiesta per impostare sfondo
@app.route('/settings_background')
def settings_background():
    global background
    # prendo background
    id_background = request.args.get('background', 0, int)
    if 3 > id_background >= 0:
        background = backgrounds[id_background]
    return render_template('settings.html')


# pagina salvataggio
@app.route('/save')
def save():
    global all_texts
    return render_template('save.html', data=zip(all_texts, all_images, all_links_img, all_links_patent, all_times, all_links_scholar))


# pagina di log
@app.route('/log')
def log():
    return logs_json


# connessione websocket
@socketio.on('tavolodelleidee')
def handle_message(msg):
    global text_global
    global all_texts
    global all_images
    global current_image
    global logs_json
    global i
    while True:
        current_keyword_info = {}
        # leggo microfono per durata seconds
        with mic as source:
            # inserimento nelle info del momento in cui si inizia ad ascoltare il discorso
            t = time.localtime()
            current_time = time.strftime("%d/%m/%Y, %H:%M:%S", t)
            current_keyword_info["time"] = current_time
            current_hour = time.strftime("%H:%M:%S", t)

            # scrittura in file json delle info del giorno
            y = time.strptime(str(t.tm_mday - 1) + "/" + str(t.tm_mon) + "/" + str(t.tm_year), "%d/%m/%Y")
            yesterday = time.strftime("%d_%m_%Y", y)
            name_file = yesterday + ".json"
            if not os.path.exists("..\\log\\" + name_file):
                with open("..\\log\\" + name_file, "w") as json_file:
                    json.dump(logs_json, json_file)
                logs_json = {}
            try:
                audio = r.record(source, duration=seconds)
            except:
                print("ok")
            # traduco il testo letto dal microfono in stringa
            try:
                if is_english():
                    text_send = r.recognize_google(audio, language="en-US")
                else:
                    text_send = r.recognize_google(audio, language="it-IT")
            except:  # non si riconosce nessun testo
                text_send = ""
            # inserimento nelle info del discorso ascoltato
            current_keyword_info["text"] = text_send
            # controllo se ci sono comandi vocali e svolgo i compiti
            #vocal_command_control(text_send)
            # filtro parole
            keyword = keyword_founder(text_send)
            # se ho trovato parole
            search_result = []
            if len(keyword) > 0:
                search_result = search(keyword)
                search_patent_result = search_patent(keyword)
                search_scholar_result = search_scholar(keyword)
                # se la ricerca della parola chiave ha trovato risultati
                if len(search_result["all_data"]["urls"]) > 0:
                    # salvo le informazioni in una lista
                    current_keyword_info["keyword"] = keyword
                    current_keyword_info["images_link"] = search_result["all_data"]["urls"]
                    current_keyword_info["pages_links"] = search_result["all_data"]["links"]
                    current_keyword_info["videos"] = search_result["all_data"]["urls_videos"]
                    logs_json[i] = current_keyword_info
                    i = i + 1
                    # aggiungo alla lista d'immagini totale da mettere nella save page
                    if len(all_texts) < 12:
                        all_texts.append(keyword)
                        all_images.append(search_result["all_data"]["urls"])
                        all_links_img.append(search_result["all_data"]["links"])
                        all_links_patent.append(search_patent_result)
                        all_links_scholar.append(search_scholar_result)
                        all_times.append(current_hour)

                    else:
                        all_texts[current_image] = keyword
                        all_images[current_image] = search_result["all_data"]["urls"]
                        all_links_img[current_image] = search_result["all_data"]["links"]
                        all_links_patent[current_image] = search_patent_result
                        all_links_scholar[current_image] = search_scholar_result
                        all_times[current_image] = current_hour
                        current_image = (current_image + 1) % 12
            # invio json delle immagini e keyword al client
            emit("response", json.dumps(search_result))



# avvio websocket con https
# socketio.run(app, host="0.0.0.0", port="443", debug=True, ssl_context=('C:\\Users\\Imaginator\\Downloads\\tavolodelleidee-master\\tavolodelleidee-master\\test\\cert.pem','C:\\Users\\Imaginator\\Downloads\\tavolodelleidee-master\\tavolodelleidee-master\\test\\pkey.pem'))
socketio.run(app, host="0.0.0.0", port="443", debug=True, ssl_context=('cert.pem', 'pkey.pem'))

# socketio.run(app, host="0.0.0.0", port="443", debug=True, ssl_context=(
# 'C:\\Users\\Imaginator\\Downloads\\tavolodelleidee-master\\tavolodelleidee-master\\test\\cert.pem',
# 'C:\\Users\\Imaginator\\Downloads\\tavolodelleidee-master\\tavolodelleidee-master\\test\\pkey.pem'))
