import os
import base64

from openai import OpenAI
from dotenv import load_dotenv
from fastapi import APIRouter, status
from fastapi.responses import StreamingResponse

from app.utility import gnerate_audio

load_dotenv()


router = APIRouter(
  prefix="/multimodel",
  tags=["multimodel"],
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')


@router.post("/", status_code=status.HTTP_202_ACCEPTED, response_class=StreamingResponse)
def multimodel():
  path = "./images/surrounding.jpeg"
  base64_image = encode_image(path)
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
    max_tokens=200,
  )
  text = response.choices[0].message.content
  return text
  # return StreamingResponse(gnerate_audio(text), media_type="audio/mpeg")

