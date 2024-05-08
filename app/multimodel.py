import os
import base64
from openai import OpenAI
from dotenv import load_dotenv
import time
from functools import wraps

from app.utility import cet


load_dotenv()



client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')


@cet
def multimodel(base64_image: str)->str:
  response = client.chat.completions.create(
    model="gpt-4-turbo",
    messages=[
      {
        "role": "user",
        "content": [  
          {"type": "text", "text": "You are an humble AI visual assistant we will provide you the images you have to Describe the image for a blind person."},
          {
            "type": "image_url",
            "image_url": {
              "url": f"data:image/jpeg;base64,{base64_image}"
            },
          },
        ],
      }
    ],
    max_tokens=300,
  )

  return response.choices[0].message.content

