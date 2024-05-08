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
    frame = frame.to_ndarray(format="bgr24") # this is for the cv logic

    while True:
        classLabelIDs, confidences, bboxs = net.detect(frame, confThreshold = 0.4)

        bboxs = list(bboxs)
        confidences = list(np.array(confidences).reshape(1,-1)[0])
        confidences = list(map(float, confidences))

        bboxIdx = cv2.dnn.NMSBoxes(bboxs, confidences, score_threshold = 0.5, nms_threshold = 0.2)
        
        object_confidences = {}

        if len(bboxIdx) != 0:
            for i in range(0, len(bboxIdx)):
                bbox = bboxs[np.squeeze(bboxIdx[i])]
                classConfidence = confidences[np.squeeze(bboxIdx[i])]
                classLabelID = np.squeeze(classLabelIDs[np.squeeze(bboxIdx[i])])
                classLabel = CLASSES[classLabelID]

                

                if classLabel not in object_confidences:
                    object_confidences[classLabel] = classConfidence
                else:
                    object_confidences[classLabel] = max(object_confidences[classLabel], classConfidence)

                classColor = [int(c) for c in COLORS[classLabelID]]

                displayText = "{}:{:.2f}".format(classLabel, classConfidence)

                x, y, w, h = bbox

                cv2.rectangle(frame, (x, y), (x + w, y + h), color=classColor, thickness=1)
                cv2.putText(frame, displayText, (x, y - 10), cv2.FONT_HERSHEY_PLAIN, 1, classColor, 2)

                object_width = w
                distance = calculate_distance(known_width=10, focal_length=280, per_width=object_width)
                cv2.putText(frame, f"Distance: {distance:.2f} cm", (x, y + h + 20), cv2.FONT_HERSHEY_PLAIN, 1, classColor, 2)

            
        return  av.VideoFrame.from_ndarray(frame, format="bgr24")



st.write("Choose the device and start the video stream")

webrtc_ctx = webrtc_streamer(
    key="object-detection",
    mode=WebRtcMode.SENDRECV,
    media_stream_constraints={"video": True, "audio": False},
    async_processing=True,
    video_frame_callback=video_frame_callback,
)

if not webrtc_ctx.state.playing:
    print("Not playing")
    st.components.v1.html("""
        <script>
    setTimeout(function() {
        var button = document.querySelector('button');
        if (button) button.click();
    }, 2000);
</script>
    """)

# Task 1: Implement the threading lock to the object detection <-- varun bhai
# Task 2: Implement the audio alert to this object detection
# Task 3: Implement the audio magic feature to the person.
# Task 4: Since, Camera Module has no code to be audio, so audio from video is the bad idea.



