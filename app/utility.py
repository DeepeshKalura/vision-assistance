import os
import time
from functools import wraps
from typing import List
import cv2
from openai import OpenAI
import requests
import numpy as np
import geocoder
from geopy.geocoders import Nominatim
#? cet = calculate_execution_time

from playaudio import playaudio



import pygame

server_address = "http://192.168.1.1"

def cet(func): 
  """
  A decorator that measures the execution time of a function.

  Args:
    func: The function to be decorated.

  Returns:
    The decorated function.

  """
  @wraps(func)
  def wrapper(*args, **kwargs):
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time of {func.__name__}: {execution_time:.3f} seconds")
    return result
  return wrapper


def capture_image():
  stream = requests.get(server_address, stream=True)
  bytes_received = bytes()
  for chunk in stream.iter_content(chunk_size=1024):
      bytes_received += chunk
      a = bytes_received.find(b'\xff\xd8') # JPEG start marker
      b = bytes_received.find(b'\xff\xd9') # JPEG end marker
      if a != -1 and b != -1:
          jpg = bytes_received[a:b+2]
          bytes_received = bytes_received[b+2:]
          frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
          cv2.imwrite('output.jpg', frame)
          break



def location_with_ip_address() -> tuple[str, list[float]]:
  """
  Retrieves the location and latitude/longitude coordinates based on the IP address of the user.

  Returns:
    A tuple containing the location (address) and latitude/longitude coordinates.

  Example:
    >>> location_with_ip_address()
    ('New York, NY, USA', [40.7128, -74.0060])
  """
  g = geocoder.ip('me')
  latlan = g.latlng
  location = g.address
  return (location, latlan)

  

def location_address_with_lat_long(lat:str, long:str):
  latlang = f"{lat}, {long}"
  geolocator = Nominatim(user_agent="help feature")
  location = geolocator.reverse(latlang)
  return location.address




client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_audio(text:str, name:str):
    a = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text,
    )
    a.write_to_file(name)

async def gnerate_audio(text:str):
    a = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text,
    )
    async for chunk in await a.aiter_bytes():
        yield chunk



def average_of_list(l:List)->float:
    """
    This function will calculate the average of the list.

    Args:
        l (List): list of numbers

    Returns:
        float: average of the list
    """
    return sum(l)/len(l)


def play_audio(file_path):
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        continue

    pygame.mixer.quit()
    pygame.quit()

def play_audio_from_audio(file_path):
  playaudio(file_path)