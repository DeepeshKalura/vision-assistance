import os
from pathlib import Path
from app.utility import cet, gnerate_audio
import google.generativeai as genai
from dotenv import load_dotenv
from fastapi import APIRouter
from fastapi.responses import FileResponse, StreamingResponse


from model_data.improved_detector import get_frame_from_receive_frames

load_dotenv()


router = APIRouter(
    prefix="/multimodel",
    tags=["multimodel"],
)


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


def extract_structured_data():
    # frame = get_frame_from_receive_frames()

    
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
    get_frame_from_receive_frames()

    
    prompt = [
       "You are an humble AI visual assistant we will provide you the image.",
       {
          "mime_type": "image/jpg",
          "data" : Path(f"output.jpg").read_bytes()
       },
       "You have to Describe the image for a blind person so that they can understand the surrounding."
    ]
    
    results = model.generate_content(prompt)
    return results.txt




@router.get("/read")
def message():
    result = extract_structured_data()
    return StreamingResponse(gnerate_audio(result), media_type="audio/mpeg")

@router.get("/describe")
def describe_surrounding():
    result = describe_surrounding()
    return StreamingResponse(gnerate_audio(result), media_type="audio/mpeg")

@router.get("fdescribe")
def describe_surrounding_faster():
    return FileResponse("/audio/general_surrounding.mp3")

