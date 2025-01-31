from tkinter import *
from tkinter.ttk import *
import random
from openai import OpenAI
import os
import sys
import json
sys.path.insert(1, os.path.abspath(os.path.join(os.path.join(os.path.abspath(__file__),".."),"..")))

from config import GPT_KEY
client = OpenAI(
    api_key= GPT_KEY,
)


window = Tk()
window.geometry("700x600")
canvas = Canvas(window, width=600, height=400, bg="white")
canvas.pack(pady=20)
canvas.create_oval(80, 60, 180, 240, width=1, fill='white')
canvas.create_oval(250, 60, 350, 240, width=1, fill='white')

left_eye = canvas.create_oval(100, 120, 140, 160, width=1, fill='black')
right_eye = canvas.create_oval(270, 120, 310, 160, width=1, fill='black')


def move_eye_left(movementx, movementy):
    canvas.moveto(left_eye,movementx,movementy)

def move_eye_right(movementx, movementy):
    canvas.moveto(right_eye,movementx,movementy)

messages = [
        {"role": "system", "content": "Genera un json con el formato {pupila1:{x,y},pupila2:{x,y}} en donde no repitas los numeros."},
        {"role": "user", "content": " Genera un json random diferente al anterior. Devuelve un unico valor de x entre 120 y 140 para pupila1. Devuelve un unico valor de x entre 290 y 310. El valor de y para pupila1 y pupila2 debe ser igual "}
    ]

def mover():

    response = client.chat.completions.create(
                        model = "gpt-3.5-turbo",
                        messages = messages,
                        temperature=0
                )
    text = response.choices[0].message.content.strip()
    messages.append({"role":"assistant","content":text})
    valor_pupilas = json.loads(text)
    print(valor_pupilas)
    move_eye_right(valor_pupilas["pupila1"]["x"],valor_pupilas["pupila1"]["y"])
    move_eye_left(valor_pupilas["pupila2"]["x"],valor_pupilas["pupila2"]["y"])
    # respuestaDeGPT.set(text)

btn = Button(window, text = 'Click me !', 
                 command = mover) 
btn.pack()

# respuestaDeGPT = StringVar()
# input_text = StringVar() 
# frm = ttk.Frame(root, padding=100)
# frm.grid()
# ttk.Label(frm, text="Mi primer chat bot").grid(column=0, row=0)
# EntradaTexto = ttk.Entry(frm, textvariable = input_text, justify = CENTER).grid(column=0, row=2) 
# textoDeCharla = ttk.Label(frm,textvariable=respuestaDeGPT).grid(column=0, row=4)





window.mainloop()




