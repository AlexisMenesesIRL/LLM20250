import os
from flask import Flask, request
import re
from datetime import datetime
import json
from openai import OpenAI
import sys
sys.path.insert(1, os.path.abspath(os.path.join(os.path.join(os.path.abspath(__file__),".."),"..")))
from config import GPT_KEY

client = OpenAI(
    api_key= GPT_KEY,
)


app = Flask(__name__, static_url_path="/", static_folder="resources")

@app.route("/")
def root():
    return app.send_static_file('index.html')

@app.route("/send_instruction",methods=['POST'])
def send_instruction():
    text = ""
    if request.method == 'POST':
        instruction = request.get_json()
        data = json.loads(instruction)
        print(data)
        response = client.chat.completions.create(
                            model = "gpt-3.5-turbo",
                            messages = [
                                {"role": "system", "content": "Vas a responder un archivo json moviendo el robot con el angulo solicitado."},
                                {"role": "user", "content": data["instruction"] }
                            ],
                            temperature=0
                    )
        text = response.choices[0].message.content.strip()
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