"""
######################
##                  ##
##      PYTHON      ##
##                  ##
######################"""

from vosk import Model, KaldiRecognizer
import speech_recognition

import os
import wave
import json
import datetime
import webbrowser

from time import sleep
from random import randint

print("""
VERSION : 0.1 
By Dima 😃""")

print("""
Новые версии всегда тут : https://github.com/Cr-e-ker/DemoAssistent-PYthon
""")

# проверка наличия модели на нужном языке в каталоге приложения
if (not os.path.exists("offline/vosk-model")):
    print("""
    Скачайте offline версию на:\nhttps://alphacephei.com/vosk/models и распакуйте в папку 'offline' под именем 'vosk-model'
    """)
    exit()

def record_and_recognize_audio(*args: tuple):
    """Запись и распознавание аудио"""
    with microphone:
        recognized_data = ""

        recognizer.adjust_for_ambient_noise(microphone, duration=2)

        try:
            print("Прослушивание...")
            audio = recognizer.listen(microphone, 5, 5)

            with open("microphone-results.wav", "wb") as file:
                file.write(audio.get_wav_data())

        except speech_recognition.WaitTimeoutError:
            print("Плохо слышно")
            return

        try:
            print("Распознание Google...")
            recognized_data = recognizer.recognize_google(audio, language="ru").lower()

        except speech_recognition.UnknownValueError:
            pass

        # в случае проблем с доступом в Интернет происходит попытка 
        # использовать offline-распознавание через Vosk
        except speech_recognition.RequestError:
            print("Офлайн распознание...")
            recognized_data = use_offline_recognition()

        return recognized_data


def use_offline_recognition():
    """
	Переключение на оффлайн-распознавание речи
    :return: распознанная фраза
	"""
    recognized_data = ""
    try:
        # анализ записанного в микрофон аудио (чтобы избежать повторов фразы)
        wave_audio_file = wave.open("microphone-results.wav", "rb")
        model = Model("offline/vosk-model-small-ru-0.22")
        offline_recognizer = KaldiRecognizer(model, wave_audio_file.getframerate())

        data = wave_audio_file.readframes(wave_audio_file.getnframes())
        if len(data) > 0:
            if offline_recognizer.AcceptWaveform(data):
                recognized_data = offline_recognizer.Result()

                recognized_data = json.loads(recognized_data)
                recognized_data = recognized_data["text"]
    except:
        print("Попробуйте ещё раз")

    return recognized_data

def command_Name(command_name: str, *args: list):
    commands = {
    ("video", "youtube", "watch", "видео") : search_youtube_video,
    ("music", "музыка", "трек", "бит", "песня") : search_music,
    ("фоновую музыку", "рандомный плейлист", "рандомный трек") : search_random_music,
    ("сколько сейчас времени", "который час", "какое время") : nowetime
    }

    for key in commands.keys():
        if command_name in key:
            commands[key](*args)
        else:
            pass

def search_youtube_video(*args: tuple):
    # if not args[0]:
    #     return

    search_term = " ".join(args[0])
    url = "https://www.youtube.com/results?search_query=" + search_term
    webbrowser.open(url)

def search_music(*args):
    music = " ".join(args[0])
    url = "https://www.youtube.com/results?search_query=" + music
    webbrowser.open(url)

def search_random_music():
    randoms_5 = randint(0, 5)

    if (randoms_5 == 1):
        webbrowser.open("https://www.youtube.com/watch?v=TdydPefLYeI")
    elif (randoms_5 == 2):
        webbrowser.open("https://www.youtube.com/watch?v=rUxyKA_-grg")
    elif (randoms_5 == 3):
        webbrowser.open("https://www.youtube.com/watch?v=jfKfPfyJRdk")
    elif (randoms_5 == 4):
        webbrowser.open("https://www.youtube.com/watch?v=-5KAN9_CzSA")
    else:
        webbrowser.open("https://www.youtube.com/watch?v=5yx6BWlEVcY")

def nowetime():
    print(datetime.datetime.now())

if __name__ == "__main__":

    recognizer = speech_recognition.Recognizer()
    microphone = speech_recognition.Microphone()

    while True:
        voice_input = record_and_recognize_audio()
        os.remove("microphone-results.wav")
        print(voice_input)

        voice_input = voice_input.split(" ")
        command = voice_input[0]

        command_options = [str(input_part) for input_part in voice_input[1:len(voice_input)]]
        command_Name(command, command_options)
