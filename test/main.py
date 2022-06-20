import json
import os.path
import time

import spacy
import speech_recognition as sr
import yake
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from py3pin.Pinterest import Pinterest

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


# inizializzazione delle variabili necessarie per utilizzare le librerie per il filtro
nlp = spacy.load("it_core_news_lg")
kw_extractor = yake.KeywordExtractor()
language = "it"
max_ngram_size = 2  # numero massimo di parole per una parola chiave
deduplication_threshold = 0.3  # una soglia di duplicazione delle parole nelle parole chiave trovate
numOfKeywords = 50  # numero massimo di parole chiave trovabili
custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_threshold,
                                            top=numOfKeywords, features=None)


def keyword_founder(audio_string):
    keywords_and_score = custom_kw_extractor.extract_keywords(audio_string)
    # copia delle parole chiave trovate dalla libreria in una lista
    keywords = []
    for kw in keywords_and_score:
        keywords.append(kw[0])

    # unisce le parole chiave singole in una stringa
    # e le parole chiave doppie vengono salvate in una lista
    sentence = ""
    sentence2 = []
    for word in keywords:
        if " " not in word:
            sentence += word + " "
        else:
            sentence2.append(word)

    # le parole chiave doppie se contengono verbi vengono eliminate
    for w in sentence2:
        doc1 = nlp(w)
        for w1 in doc1:
            if w1.pos_ == 'VERB':
                if w in keywords:
                    keywords.remove(w)

    # le parole chiave singole se non sono nomi vengono eliminate
    doc = nlp(sentence)
    for word in doc:
        if word.pos_ != 'NOUN':
            if word.text in keywords:
                keywords.remove(word.text)

    if len(keywords) > 0:
        return keywords[-1]
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
    return render_template('save.html', data=zip(all_texts, all_images, all_times))


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
            if not os.path.exists("C:\\Users\\Imaginator\\Downloads\\tavolodelleidee-master\\tavolodelleidee-master\\log\\" + name_file):
                with open("C:\\Users\\Imaginator\\Downloads\\tavolodelleidee-master\\tavolodelleidee-master\\log\\" + name_file, "w") as json_file:
                    json.dump(logs_json, json_file)
                logs_json = {}

            audio = r.record(source, duration=seconds)
            # traduco il testo letto dal microfono in stringa
            try:
                text_send = r.recognize_google(audio, language="it-IT")
            except sr.UnknownValueError:  # non si riconosce nessun testo
                text_send = ""
            # inserimento nelle info del discorso ascoltato
            current_keyword_info["text"] = text_send
            # filtro parole
            keyword = keyword_founder(text_send)
            # se ho trovato parole
            search_result = []
            if len(keyword) > 0:
                search_result = search(keyword)
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
                        all_images.append(search_result["all_data"]["urls"][0])
                        all_times.append(current_hour)
                    else:
                        all_texts[current_image] = keyword
                        all_images[current_image] = search_result["all_data"]["urls"][0]
                        all_times[current_image] = current_hour
                        current_image = (current_image + 1) % 12
            # invio json delle immagini e keyword al client
            emit("response", json.dumps(search_result))


# avvio websocket con https
socketio.run(app, host="0.0.0.0", port="443", debug=True, ssl_context=('C:\\Users\\Imaginator\\Downloads\\tavolodelleidee-master\\tavolodelleidee-master\\test\\cert.pem','C:\\Users\\Imaginator\\Downloads\\tavolodelleidee-master\\tavolodelleidee-master\\test\\pkey.pem'))
# socketio.run(app, host="0.0.0.0", port="443", debug=True, ssl_context=('cert.pem', 'pkey.pem'))

# socketio.run(app, host="0.0.0.0", port="443", debug=True, ssl_context=(
# 'C:\\Users\\Imaginator\\Downloads\\tavolodelleidee-master\\tavolodelleidee-master\\test\\cert.pem',
# 'C:\\Users\\Imaginator\\Downloads\\tavolodelleidee-master\\tavolodelleidee-master\\test\\pkey.pem'))
