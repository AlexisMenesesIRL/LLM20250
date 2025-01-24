import os
from flask import Flask
import re
from datetime import datetime
import json

app = Flask(__name__, static_url_path="/", static_folder="resources")

@app.route("/")
def root():
    return app.send_static_file('index.html')

@app.route("/get_dialog/<nombre>&<apellido>")
def processar_dialog(nombre,apellido):
    return json.dumps({"response":"Nuestro cliente es " + nombre + " " + apellido})
    


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