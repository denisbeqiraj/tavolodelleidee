import speech_recognition as sr
import asyncio
import websockets
import yake
import spacy

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
            keywords.remove(word.text)
    return keywords


r = sr.Recognizer()
mic = sr.Microphone(device_index=0)


async def echo(websocket):
    async for message in websocket:
        with mic as source:
            audio = r.record(source, duration=10)
            text_send = ""
            try:
                text_send = r.recognize_google(audio, language="it-IT")
            except:
                text_send = ""
            keyword = keyword_founder(text_send)
            await websocket.send(keyword)


start_server = websockets.serve(echo, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
