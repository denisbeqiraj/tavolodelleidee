import json
import logging
import re
import time

import requests
import spacy
import speech_recognition as sr
import yake
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)

socketio = SocketIO(app, cors_allowed_origins='*')

logger = logging.getLogger(__name__)

text_global = ""
logs_json = {}
i = 0
seconds = 10
all_texts = []
all_images = []
current_image = 0
background = "wood.png"
backgrounds = ["wood.png", "white.png", "black.png"]


# Search keyword
def search(keywords):
    url = 'https://duckduckgo.com/'
    params = {
        'q': keywords
    }

    #   First make a request to above URL, and parse out the 'vqd'
    #   This is a special token, which should be used in the subsequent request
    res = requests.post(url, data=params)
    search_obj = re.search(r'vqd=([\d-]+)\&', res.text, re.M | re.I)

    if not search_obj:
        logger.error("Token Parsing Failed !")
        return -1

    headers = {
        'authority': 'duckduckgo.com',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'sec-fetch-dest': 'empty',
        'x-requested-with': 'XMLHttpRequest',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'referer': 'https://duckduckgo.com/',
        'accept-language': 'en-US,en;q=0.9',
    }

    params = (
        ('l', 'us-en'),
        ('o', 'json'),
        ('q', keywords),
        ('vqd', search_obj.group(1)),
        ('f', ',,,'),
        ('p', '1'),
        ('v7exp', 'a'),
    )

    request_url = url + "i.js"

    data_receive = []
    while True:
        try:
            res = requests.get(request_url, headers=headers, params=params)
            data = json.loads(res.text)
            break
        except ValueError as e:
            time.sleep(5)
            continue

    objs = data["results"]
    for obj in objs:
        data_receive.append(obj["image"])
    return data_receive


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

    search_word = []
    if len(keywords) > 0:
        search_word = search(keywords[0])
    word_send = ""
    image_number = 5
    if len(search_word) >= image_number:
        for k in search_word[:image_number]:
            word_send = word_send + k + ","
    data = {
        "all_data": {
            "word": keywords,
            "link": search_word[:image_number]
        }
    }
    return data


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
    return render_template('save.html', data=zip(all_texts, all_images))


# pagina di log
@app.route('/log')
def log():
    return logs_json


# connessione websocket
@socketio.on('tavolodelleidee')
def handleMessage(msg):
    global text_global
    global all_texts
    global all_images
    global current_image
    global i
    while True:
        current_keyword_info = {}
        # leggo microfono per durata seconds
        with mic as source:
            try:
                t = time.localtime()
                current_time = time.strftime("%H:%M:%S", t)
                current_keyword_info["time"] = current_time
                audio = r.record(source, duration=seconds)
            except:
                print("ok")
            # traduco il testo letto dal microfono in stringa
            try:
                text_send = r.recognize_google(audio, language="it-IT")
            except:
                text_send = ""
            current_keyword_info["text"] = text_send
            # print(text_send)
            # filtro parole
            keyword = keyword_founder(text_send)
            # se ho trovato parole
            if len(keyword["all_data"]["word"]) > 0 and len(keyword["all_data"]["link"]) > 0:
                text_global = keyword["all_data"]["word"][0]
                current_keyword_info["keyword"] = text_global
                current_keyword_info["images_link"] = keyword["all_data"]["link"]
                logs_json[i] = current_keyword_info
                i = i + 1
                # aggiungo alla lista d'immagini
                if len(all_texts) < 12:
                    all_texts.append(keyword["all_data"]["word"][0])
                    all_images.append(keyword["all_data"]["link"][0])
                else:
                    all_texts[current_image] = keyword["all_data"]["word"][0]
                    all_images[current_image] = keyword["all_data"]["link"][0]
                    current_image = (current_image + 1) % 12
            # invio json delle immagini e keyword al client
            emit("response", json.dumps(keyword))


# avvio websocket con https
socketio.run(app, host="0.0.0.0", port="443", debug=True, ssl_context=('C:\\Users\\Imaginator\\Downloads\\tavolodelleidee-master\\tavolodelleidee-master\\test\\cert.pem','C:\\Users\\Imaginator\\Downloads\\tavolodelleidee-master\\tavolodelleidee-master\\test\\pkey.pem'))
