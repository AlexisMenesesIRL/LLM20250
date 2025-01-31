from tkinter import *
from tkinter import ttk
from openai import OpenAI
import os
import sys
sys.path.insert(1, os.path.abspath(os.path.join(os.path.join(os.path.abspath(__file__),".."),"..")))

from config import GPT_KEY
client = OpenAI(
    api_key= GPT_KEY,
)


root = Tk()

respuestaDeGPT = StringVar()
input_text = StringVar() 
frm = ttk.Frame(root, padding=100)
frm.grid()
ttk.Label(frm, text="Mi primer chat bot").grid(column=0, row=0)
EntradaTexto = ttk.Entry(frm, textvariable = input_text, justify = CENTER).grid(column=0, row=2) 
textoDeCharla = ttk.Label(frm,textvariable=respuestaDeGPT).grid(column=0, row=4)


def hablar():
    response = client.chat.completions.create(
                        model = "gpt-3.5-turbo",
                        messages = [
                            {"role": "system", "content": "Cada vez que te de un nombre, quiero que describas cualidades hermosas y fascinantes en base a ese nombre."},
                            {"role": "user", "content": input_text.get()}
                        ],
                        temperature=0
                )
    text = response.choices[0].message.content.strip()
    respuestaDeGPT.set(text)

ttk.Button(frm, text="Enviar", command=hablar).grid(column=0, row=6)
root.mainloop()




