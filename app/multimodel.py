import os
from pathlib import Path
import google.generativeai as genai
from PIL import Image
import base64
from openai import OpenAI
from dotenv import load_dotenv
from app.utility import capture_image, capture_image_with_pc_camera

load_dotenv()


client =  OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def encode_image(image_path = "output.jpg"):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')
  


def describe_surrounding_with_open_ai():
  base64_image = encode_image()
  completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
      {
         "role": "system",
          "content":"You are an humble AI visual assistant we will provide you the image. You have to Describe the image for a blind person so that they can understand the surrounding.",
      },  
      {
         "role" : "user",
         "content": [
            {
               "type": "image_url",
               "image_url": {
                  "url": f"data:image/jpeg;base64,{base64_image}"
               }
            }
         ] 
      }    
    ]

    
  )

  return completion.choices[0].message.content



# google gemini clinet !  No more free api
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Set up the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 0,
  "max_output_tokens": 8192,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

model = genai.GenerativeModel(model_name="gemini-1.0-pro-vision-latest",
                              generation_config=generation_config,
                              safety_settings=safety_settings)


def read_image():
    # capture_image()
    capture_image_with_pc_camera()
    
    prompt = [
       "You are an expert admin people who will extract core information from documents",
       {
          "mime_type": "image/jpeg",
          "data" : Path(f"output.jpg").read_bytes()
       },
       "You are the best OCR in this world, please provide text to the blind person being accurate is yout goal:"
    ]
    
    results = model.generate_content(prompt)
    return results.text


def describe_surrounding():
    # capture_image()
    capture_image_with_pc_camera()

    
    prompt = [
       "You are an humble AI visual assistant we will provide you the image.",
       {
          "mime_type": "image/jpg",
          "data" : Path(f"output.jpg").read_bytes()
       },
       "You have to Describe the image for a blind person so that they can understand the surrounding."
    ]
    
    results = model.generate_content(prompt)
    return results.text


# Note i see i have to comment the changes when i have to switch from the camera_module or simple pc camera
# so this can be done through dependencies injection design pattern in the code
# so we need to switch all of this code to class for dependencies have to follow depencies injection techique 


