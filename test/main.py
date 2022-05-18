import speech_recognition as sr
import yake
import spacy
import requests
import re
import json
import time
import logging
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, send

app = Flask(__name__)

socketio = SocketIO(app, cors_allowed_origins='*')

logger = logging.getLogger(__name__)

text_global = ""
seconds = 10
all_texts = []
all_images = []
current_image = 0
background = "wood.png"
backgrounds = ["wood.png", "black.png", "white.png"]

//Search keyword
def search(keywords, max_results=None):
    url = 'https://duckduckgo.com/'
    params = {
        'q': keywords
    }

    #   First make a request to above URL, and parse out the 'vqd'
    #   This is a special token, which should be used in the subsequent request
    res = requests.post(url, data=params)
    searchObj = re.search(r'vqd=([\d-]+)\&', res.text, re.M | re.I)

    if not searchObj:
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
        ('vqd', searchObj.group(1)),
        ('f', ',,,'),
        ('p', '1'),
        ('v7exp', 'a'),
    )

    requestUrl = url + "i.js"

    data_receive = []
    while True:
        try:
            res = requests.get(requestUrl, headers=headers, params=params)
            data = json.loads(res.text)
            break
        except ValueError as e:
            time.sleep(5)
            continue

    objs = data["results"]
    for obj in objs:
        data_receive.append(obj["image"])
    return data_receive


'''
r = sr.Recognizer()
        mic = sr.Microphone()
        print(sr.Microphone.list_microphone_names())
        mic = sr.Microphone(device_index=0)
        with mic as source:
            audio = r.record(source, duration=5)
        text_send=""
        try:
            text_send = r.recognize_google(audio, language="it-IT")
        except:
            text_send = ""
'''

# inizializzazione delle variabili necessarie per utilizzare le librerie per il filtro
nlp = spacy.load("it_core_news_lg")
kw_extractor = yake.KeywordExtractor()
language = "it"
max_ngram_size = 2 #numero massimo di parole per una parola chiave
deduplication_threshold = 0.3 #una soglia di duplicazione delle parole nelle parole chiave trovate
numOfKeywords = 50 #numero massimo di parole chiave trovabili
custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_threshold,
                                            top=numOfKeywords, features=None)


def keyword_founder(audio_string):
    keywords_and_score = custom_kw_extractor.extract_keywords(audio_string)
    #copia delle parole chiave trovate dalla libreria in una lista
    keywords = []
    for kw in keywords_and_score:
        keywords.append(kw[0])

    #unisce le parole chiave singole in una stringa
    #e le parole chiave doppie vengono salvate in una lista
    sentence = ""
    sentence2 = []
    for word in keywords:
        if " " not in word:
            sentence += word + " "
        else:
            sentence2.append(word)

    #le parole chiave doppie se contengono verbi vengono eliminate
    for w in sentence2:
        doc1 = nlp(w)
        for w1 in doc1:
            if w1.pos_ == 'VERB':
                if w in keywords:
                    keywords.remove(w)

    #le parole chiave singole se non sono nomi vengono eliminate
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

//index.html con sfondo
@app.route('/')
def index():
    global background
    return render_template('index.html', background_value="../static/image_background/" + background)

//pagina settings
@app.route('/settings')
def settings():
    return render_template('settings.html')

//richiesta per impostare parametri
@app.route('/settings_parameters')
def settings_parameters():
    global seconds
    //prendo secondi
    try:
        seconds = int(request.args.get('seconds'))
    except:
        print("error")
    //prendo background
    background = int(request.args.get('image_background'))
    if 3 > background >= 0:
        background = backgrounds[background]

    return render_template('settings.html')

//pagina salvataggio
@app.route('/save')
def save():
    global all_texts
    return render_template('save.html', data=zip(all_texts, all_images))

//connessione websocket
@socketio.on('tavolodelleidee')
def handleMessage(msg):
    global text_global
    global all_texts
    global all_images
    global current_image
    while True:
        //leggo microfono per durata seconds
        with mic as source:
            try:
                audio = r.record(source, duration=seconds)
            except:
                print("ok")
            //traduco il testo letto dal microfono in stringa
            text_send = ""
            try:
                text_send = r.recognize_google(audio, language="it-IT")
            except:
                text_send = ""
            print(text_send)
            //filtro parole
            keyword = keyword_founder(text_send)
            //se ho trovato parole
            if len(keyword["all_data"]["word"]) > 0 and len(keyword["all_data"]["link"]) > 0:
                text_global = keyword["all_data"]["word"][0]
                //aggiungo alla lista di immagini
                if len(all_texts) < 12:
                    all_texts.append(keyword["all_data"]["word"][0])
                    all_images.append(keyword["all_data"]["link"][0])
                else:
                    all_texts[current_image] = keyword["all_data"]["word"][0]
                    all_images[current_image] = keyword["all_data"]["link"][0]
                    current_image = (current_image + 1) % 12
            //invio json delle immagini e keyword al client
            emit("response", json.dumps(keyword))

//avvio websocket con https
socketio.run(app, host="0.0.0.0", port="443", debug=True,ssl_context=('C:\\Users\\Imaginator\\Downloads\\tavolodelleidee-master\\tavolodelleidee-master\\test\\cert.pem','C:\\Users\\Imaginator\\Downloads\\tavolodelleidee-master\\tavolodelleidee-master\\test\\pkey.pem'))
