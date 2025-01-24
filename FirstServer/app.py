import os
from flask import Flask
import re
from datetime import datetime
import json
import config
import openai
openai.api_key = config.GPT_KEY


app = Flask(__name__, static_url_path="/", static_folder="resources")

@app.route("/")
def root():
    return app.send_static_file('index.html')

@app.route("/get_dialog/<nombre>&<apellido>")
def processar_dialog(nombre,apellido):
    response = openai.ChatCompletion.create(
                        model = "gpt-3.5-turbo-16k-0613",
                        messages = [
                            {"role": "system", "content": "Eres un agente virtual que nos dira una descripción basado en el nombre que te daremos."},
                            {"role": "user", "content": "mi nombre es "+ nombre + " " + apellido }
                        ],
                        temperature=0
                )
    text = response['choices'][0]['message']['content']
    return json.dumps({"response":text})
    


@app.route("/hello/<name>")
def hello_there(name):
    now = datetime.now()
    formatted_now = now.strftime("%A, %d %B, %Y at %X")

    # Filter the name argument to letters only using regular expressions. URL arguments
    # can contain arbitrary text, so we restrict to safe characters only.
    match_object = re.match("[a-zA-Z]+", name)

    if match_object:
        clean_name = match_object.group(0)
    else:
        clean_name = "Friend"

    content = "Hello there, " + clean_name + "! It's " + formatted_now
    return content

if __name__ == "__main__":
    app.run(host=os.getenv("APP_ADDRESS", 'localhost'), \
    port=os.getenv("APP_PORT", 80))