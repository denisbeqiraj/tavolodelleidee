import speech_recognition as sr
import asyncio
import websockets
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
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins='*')

logger = logging.getLogger(__name__)

text_global = ""
seconds = 10
all_texts = []
all_images = []
current_image = 0


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

nlp = spacy.load("it_core_news_lg")
kw_extractor = yake.KeywordExtractor()
language = "it"
max_ngram_size = 2
deduplication_threshold = 0.3
numOfKeywords = 50
custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_threshold,
                                            top=numOfKeywords, features=None)


def keyword_founder(audio_string):
    keywords_and_score = custom_kw_extractor.extract_keywords(audio_string)
    keywords = []
    for kw in keywords_and_score:
        keywords.append(kw[0])

    sentence = ""
    for word in keywords:
        if " " not in word:
            sentence += word + " "

    doc = nlp(sentence)
    for word in doc:
        if word.pos_ != 'NOUN':
            try:
                keywords.remove(word.text)
            except:
                print("")
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


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/settings')
def settings():
    return render_template('settings.html')


@app.route('/settings_parameters')
def settings_parameters():
    global seconds
    seconds = int(request.args.get('seconds'))
    return render_template('settings.html')


@app.route('/save')
def save():
    global all_texts
    return render_template('save.html', data=zip(all_texts, all_images))


@socketio.on('tavolodelleidee')
def handleMessage(msg):
    global text_global
    global all_texts
    global all_images
    global current_image
    while True:
        with mic as source:
            try:
                audio = r.record(source, duration=seconds)
            except:
                print("ok")
            text_send = ""
            try:
                text_send = r.recognize_google(audio, language="it-IT")
            except:
                text_send = ""
            print(text_send)
            keyword = keyword_founder(text_send)
            if len(keyword["all_data"]["word"]) > 0 and len(keyword["all_data"]["link"]) > 0:
                text_global = keyword["all_data"]["word"][0]
                if len(all_texts) < 12:
                    all_texts.append(keyword["all_data"]["word"][0])
                    all_images.append(keyword["all_data"]["link"][0])
                else:
                    all_texts[current_image] = keyword["all_data"]["word"][0]
                    all_images[current_image] = keyword["all_data"]["link"][0]
                    current_image = (current_image + 1) % 12

            emit("response", json.dumps(keyword))


socketio.run(app, port=2000)
