import cv2 
import av
import numpy as np
import streamlit as st
from collections import deque
from streamlit_webrtc import webrtc_streamer, WebRtcMode


st.title('Obstacle Detection System')


CLASSES = []
with open("./model_data/coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

@st.cache_resource  
def generate_label_colors():
    return np.random.uniform(0, 255, size=(len(CLASSES), 3))


COLORS = generate_label_colors()



cache_key = "object_detection_dnn"
if cache_key in st.session_state:
    net = st.session_state[cache_key]
else:
    net = cv2.dnn_DetectionModel('./model_data/frozen_inference_graph.pb', './model_data/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt')
    net.setInputSize(320, 320)
    net.setInputScale(1.0 / 127.5)
    net.setInputMean((127.5, 127.5, 127.5))
    net.setInputSwapRB(True)
    st.session_state[cache_key] = net




classes = []
with open("./model_data/coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]


def calculate_distance(known_width, focal_length, per_width):
        return (known_width * focal_length) / per_width

def video_frame_callback(frame:av.AudioFrame)->av.VideoFrame:
    pass



st.write("Choose the device and start the video stream")

webrtc_ctx = webrtc_streamer(
    key="object-detection",
    mode=WebRtcMode.SENDRECV,
    media_stream_constraints={"video": True, "audio": False},
    async_processing=True,
    video_frame_callback=video_frame_callback,
)

