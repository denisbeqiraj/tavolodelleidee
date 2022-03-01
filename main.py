import speech_recognition as sr
import asyncio
import websockets

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

r = sr.Recognizer()
mic = sr.Microphone(device_index=0)


async def echo(websocket):
    async for message in websocket:
        with mic as source:
            audio = r.record(source, duration=10)
            text_send=""
            try:
                text_send = r.recognize_google(audio, language="it-IT")
            except:
                text_send = ""
            await websocket.send(text_send)


start_server = websockets.serve(echo, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
