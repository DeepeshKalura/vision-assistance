# Program to read frames from http server made by Realtek AMB82 mini iot camera module .


import cv2
import requests
import numpy as np

# HTTP server address
server_address = "http://192.168.1.1" # Change with your router/IP address.

# Function to receive frames from the HTTP server
def receive_frames():
    url = server_address
    stream = requests.get(url, stream=True)
    bytes_received = bytes()
    for chunk in stream.iter_content(chunk_size=1024):
        bytes_received += chunk
        a = bytes_received.find(b'\xff\xd8') # JPEG start marker
        b = bytes_received.find(b'\xff\xd9') # JPEG end marker
        if a != -1 and b != -1:
            jpg = bytes_received[a:b+2]
            bytes_received = bytes_received[b+2:]
            frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
            yield frame

# Display frames
def display_frames():
    for frame in receive_frames():
        cv2.imshow('Frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Main function
def main():
    display_frames()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
