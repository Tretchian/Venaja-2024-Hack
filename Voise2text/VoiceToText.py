import subprocess
from vosk import Model, KaldiRecognizer
from pydub import AudioSegment
import json
import os

def convert_ogg_to_wav(odd, wav):
     #Путь к проге для конвертации
     #cleaffmpeg_path = r"/home/tretchian/projects/Venaja-2024-Hack/Voise-2-text/FFmpeg/ffmpeg.exe"
     #Команда для консоли
    #  command = ['ffmpeg', "-i", ogg_file, wav_file]
    command = ['ffmpeg', "-i", odd, wav]
     #command = ['ffmpeg', "-i", ogg_file, wav_file]
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

    #rec.SetWords(True)

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
    

'''
def main():
    #Имя голосового сообщения
    name_audio_file = r"ttk"

    #Путь до гс.ogg и гс.wav
    ogg_file_path = "audiofile" + name_audio_file + '.ogg'
    wav_file_path = "audiofile" + name_audio_file + '.wav'

    #Вызов функции конвертации формата гс
    convert_ogg_to_wav(ogg_file_path, wav_file_path)

    #Вызов функции транскрибции
    #print(Voise_to_text(name_audio_file))

    #Удаление гс
    #os.remove(ogg_file_path)
    #os.remove(wav_file_path)

if __name__ == "__main__":
    main()

'''