from tkinter import *
from tkinter import ttk
from openai import OpenAI
import config 
client = OpenAI(
    api_key=config.GPT_KEY,
)


root = Tk()
def hablar():
    response = client.chat.completions.create(
                        model = "gpt-3.5-turbo",
                        messages = [
                            {"role": "system", "content": "Cada vez que te de un nombre, quiero que describas cualidades hermosas y fascinantes en base a ese nombre."},
                            {"role": "user", "content": "presentate"}
                        ],
                        temperature=0
                )
    text = response.choices[0].message.content.strip()
    respuestaDeGPT.set(text)
respuestaDeGPT = StringVar()
frm = ttk.Frame(root, padding=100)
frm.grid()
ttk.Label(frm, text="Mi primer chat bot").grid(column=0, row=0)
textoDeCharla = ttk.Label(frm,textvariable=respuestaDeGPT).grid(column=0, row=2)

ttk.Button(frm, text="Enviar", command=hablar).grid(column=0, row=4)
root.mainloop()




