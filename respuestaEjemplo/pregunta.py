from tkinter import *
import random
from openai import OpenAI
import os
import sys
import json
import time
sys.path.insert(1, os.path.abspath(os.path.join(os.path.join(os.path.abspath(__file__),".."),"..")))

from config import GPT_KEY
client = OpenAI(
    api_key= GPT_KEY,
)

win=Tk()
win.geometry("700x700")
emocion=Text(win, height=5, width=40)
emocion.pack()

messages = [
        {"role": "system", "content": "Genera una frase con la palabra."},
    ]

def recibir_respuesta():

    response = client.chat.completions.create(
                        model = "gpt-3.5-turbo",
                        messages = messages,
                        temperature=0
                )
    text = response.choices[0].message.content.strip()
    messages.append({"role":"assistant","content":text})
    for character in text:
        print(character)
        if character in ["a","i","o","u","e"]:
            print(os.path.dirname(__file__)+"/"+character+".png")
            new_image = PhotoImage(file=os.path.dirname(__file__)+"/"+character+".png")
            image_label.configure(image= new_image)
            image_label.image = new_image   
            win.update_idletasks()
        else:
            new_image = PhotoImage(file=os.path.dirname(__file__)+"/n.png")
            image_label.configure(image= new_image)
            image_label.image = new_image    
            win.update_idletasks()
        time.sleep(1) 
    


image = PhotoImage(file=os.path.dirname(__file__)+"/n.png")
image_label = Label(win, image=image)
image_label.pack()

def enviar_solicitud():
    value=emocion.get("1.0","end-1c")
    messages.append({"role":"user","content":value})
    recibir_respuesta()

comment= Button(win, height=5, width=10, text="Comment", command=lambda: enviar_solicitud())
comment.pack()




win.mainloop()