# 한국어 버전

import speech_recognition as sr
import webbrowser
import time
import playsound
import os
import random
from gtts import gTTS
from time import ctime
from datetime import datetime

r = sr.Recognizer()

# today = date.today()
now = datetime.now()

def record_audio(ask = False):
    with sr.Microphone() as source:
        if ask:
            alexis_speak(ask)
        audio = r.listen(source)
        voice_data = ''
        try:
            voice_data = r.recognize_google(audio, language='ko-KR')
        except sr.UnknownValueError:
            # print('Sorry, I did not get that')
            alexis_speak('죄송하지만 잘 못 들었습니다, 다시 한 번 말해주세요.')
        except sr.RequestError:
            # print('Sorry, my speech service is down')
            alexis_speak('죄송합니다. 서비스에 문제가 있습니다.')
        return voice_data


def alexis_speak(audio_string):
    tts = gTTS(text=audio_string, lang='ko')
    r = random.randint(1, 10000000)
    audio_file = 'audio-' + str(r) + '.mp3'
    tts.save(audio_file)
    playsound.playsound(audio_file)
    print(audio_string)
    os.remove(audio_file)


def respond(voice_data):
    if '이름' in voice_data:
        alexis_speak('제 이름은 알렉시스입니다.')
    if '시간' in voice_data or '날짜' in voice_data:
        alexis_speak(now.strftime('%Y년 %m월 %d일 %A %p %I시 %M분입니다.'))
    if '검색' in voice_data:
        search = record_audio('어떤 것을 검색해 드릴까요?')
        url = 'https://google.com/search?q=' + search
        webbrowser.get().open(url)
        alexis_speak(search + '를 검색한 결과입니다.')
    if '장소' in voice_data or '위치' in voice_data:
        location = record_audio('어디를 찾아드릴까요?')
        url = 'https://google.nl/maps/place/' + location + '/&amp;'
        webbrowser.get().open(url)
        alexis_speak(location + '를 지도에서 찾은 결과입니다.')
    if '종료' in voice_data or '끝' in voice_data:
        alexis_speak('안녕히가세요.')
        exit()


time.sleep(1)
alexis_speak('무엇을 도와드릴까요?')
while 1:
    voice_data = record_audio()
    respond(voice_data)