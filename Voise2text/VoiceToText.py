import subprocess
from vosk import Model, KaldiRecognizer
from pydub import AudioSegment
import json
import os

def convert_ogg_to_wav(odd, wav):
     #Путь к проге для конвертации
     #Команда для консоли
    command = ['ffmpeg', "-i", odd, wav]
     #Запуск консоли и выполнение команды
    subprocess.run(command)


def Voise_to_text(namefile):
    
    ogg_file_path = namefile + '.ogg'
    wav_file_path = namefile + '.wav'
    convert_ogg_to_wav(ogg_file_path, wav_file_path)

    model = Model(r"/home/tretchian/projects/Venaja-2024-Hack/Voise2text/model/vosk-model-small-ru-0.22")
    # Устанавливаем Frame Rate
    FRAME_RATE = 16000
    #Подключение модели транскрипции
    rec = KaldiRecognizer(model, FRAME_RATE)

    # Используя библиотеку pydub делаем предобработку аудио
    mp3 = AudioSegment.from_file(wav_file_path)
    mp3 = mp3.set_channels(1)
    mp3 = mp3.set_frame_rate(FRAME_RATE)

    # Преобразуем вывод в json
    rec.AcceptWaveform(mp3.raw_data)
    result = rec.Result()
    text = json.loads(result)["text"]
    os.remove(ogg_file_path)
    os.remove(wav_file_path) 
    return text
    
