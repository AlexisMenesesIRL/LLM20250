import base64
import cv2
from openai import OpenAI
import sys
import os
sys.path.insert(1, os.path.abspath(os.path.join(os.path.join(os.path.abspath(__file__),".."),"..")))
from config import GPT_KEY
client = OpenAI(
    api_key= GPT_KEY,
)

camera = cv2.VideoCapture(0)
for i in range(180):
    return_value, image = camera.read()
    cv2.imwrite('images.jpg', image)
del(camera)

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


# Path to your image
image_path = "images.jpg"

# # # Getting the Base64 string
base64_image = encode_image(image_path)

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Describe the image in spanish",
                },
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                },
            ],
        }
    ],
)
print(response.choices[0].message.content)