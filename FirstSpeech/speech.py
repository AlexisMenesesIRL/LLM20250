import torch
import pygame
from TTS.api import TTS
from openai import OpenAI
import sys
import os
import tempfile
import sounddevice as sd
import soundfile as sf
import time
from langdetect import detect
from langdetect import detect_langs
pygame.init()


device = "cuda" if torch.cuda.is_available() else "cpu"
sys.path.insert(1, os.path.abspath(os.path.join(os.path.join(os.path.abspath(__file__),".."),"..")))

tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

from config import GPT_KEY

client = OpenAI(
    api_key= GPT_KEY,
)

duration = 5
frequency = 44100
channels = 1
print("Empieza a hablar")

recording = sd.rec(int(frequency*duration),samplerate = frequency, channels = channels,blocking=True)
sd.wait()
with tempfile.NamedTemporaryFile(suffix=".wav",delete=False) as temp_audio:
    sf.write(temp_audio.name,recording,frequency)
    temp_audio.seek(0)
file = open(temp_audio.name,"rb")
transcription = client.audio.transcriptions.create(
    model="whisper-1", 
    file=file
)
response = client.chat.completions.create(
                    model = "gpt-3.5-turbo",
                    messages = [
                        {"role": "system", "content": "Eres un avatar que respondera a lo que diga el usuario. Las fechas escribelas con alfabeto (como se lee)."},
                        {"role": "user", "content": transcription.text }
                    ],
                    temperature=0
            )

text = response.choices[0].message.content.strip()
print("esperaremos "  + str(len(text)*0.2)+ " segundos")
wav = tts.tts_to_file(text=text, file_path="ejemplo.wav")
pygame.mixer.music.load("ejemplo.wav")
pygame.mixer.music.play()
pygame.event.wait()
time.sleep(len(text)*0.2)

#Clonar tu propia voz
# text = "hola, esto es una prueba para poder verificar que el tts esta hablando como yo quiero."
# tts.tts_to_file(text=text, speaker_wav="vozVictorEcheverria.wav", language=detect(text),
#                     file_path="example.wav")