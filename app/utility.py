import time
from functools import wraps
import cv2
import requests
import numpy as np
import geocoder
import webbrowser
#? cet = calculate_execution_time


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


def iot_to_cv_server():
  url = "http://192.168.164.45/"
  jpeg_stream = requests.get(url, stream=True)

  if jpeg_stream.status_code == 200:
    bytes_data = bytes()
    for chunk in jpeg_stream.iter_content(chunk_size=1024):
        bytes_data += chunk
        a = bytes_data.find(b'\xff\xd8')
        b = bytes_data.find(b'\xff\xd9')
        if a != -1 and b != -1:
            jpg = bytes_data[a:b+2]
            bytes_data = bytes_data[b+2:]
            frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
            if frame is not None:
                    yield frame
  else:
      raise ConnectionError(f"Failed to connect to the server with status code: {jpeg_stream.status_code}")



def location_with_ip_address()->tuple[str, list[float]]:
    g = geocoder.ip('me')
    latlan = g.latlng
    location = g.address
    return (location, latlan)

  

def location_with_gps():
  pass