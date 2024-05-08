import cv2
import numpy as np
import requests

stream_url = 'http://192.168.137.246/'  # Replace this with your server URL

# Function to read JPEGs from HTTP stream
def read_jpeg_stream(url):
    # Open the stream
    stream = requests.get(url, stream=True)
    if stream.status_code == 200:
        bytes_data = bytes()
        for chunk in stream.iter_content(chunk_size=1024):
            bytes_data += chunk
            a = bytes_data.find(b'\xff\xd8')
            b = bytes_data.find(b'\xff\xd9')
            if a != -1 and b != -1:
                jpg = bytes_data[a:b + 2]
                bytes_data = bytes_data[b + 2:]
                yield cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
    else:
        print("Failed to open stream")

# Main function to display the stream
def display_stream(url):
    cap = read_jpeg_stream(url)
    while True:
        frame = next(cap)
        cv2.imshow('Frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()

if __name__ == "__main__":
    display_stream(stream_url)
