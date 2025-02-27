import pygame
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

sys.path.insert(1, os.path.abspath(os.path.join(os.path.join(os.path.abspath(__file__),".."),"..")))

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
print(transcription)
response = client.chat.completions.create(
                    model = "gpt-3.5-turbo",
                    messages = [
                        {"role": "system", "content": "Eres un avatar que respondera a lo que diga el usuario. Las fechas escribelas con alfabeto (como se lee)."},
                        {"role": "user", "content": transcription.text }
                    ],
                    temperature=0
            )

text = response.choices[0].message.content.strip()

