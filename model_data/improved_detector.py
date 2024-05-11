import time
import cv2
import numpy as np
import requests
import threading

KNOWN_WIDTHS = {
    "person": 0.5,
    "car": 2,
    "backpack" : 0.55,
    "bottle" : 0.20,
    "cup" : 0.15,
    "chair" : 0.50,
    "laptop" : 0.40,
    "mouse" : 0.10,
    "keyboard" : 0.30,
    "phone" : 0.15,  
}
objects_within_distance = {}

def read_classes(classesPath):
    with open(classesPath, 'r') as f:
        classesList = f.read().splitlines()

    classesList.insert(0, '__Background__')
    colorList = np.random.uniform(low=0, high=255, size=(len(classesList),3))

    return classesList, colorList

def calculate_distance(known_width, focal_length, per_width):
    return (known_width * focal_length) / per_width


modelPath = "model_data/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
configPath = "model_data/frozen_inference_graph.pb"
net = cv2.dnn_DetectionModel(modelPath, configPath)
net.setInputSize(320,320)
net.setInputScale(1.0/127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

known_width = 10
focal_length = 280
classesPath = "model_data/coco.names"
classesList, colorList = read_classes(classesPath)
server_address = "http://192.168.1.1"


def receive_frames(self):
    stream = requests.get(self.server_address, stream=True)
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


def generting_alert(alert:str):
    import requests
    requests.post('http://localhost:8000/stream/alert', data = {'message': alert})
    

    

def get_frame_from_receive_frames():
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
def distance_to_camera( known_width, per_width, focal_Length):
        return (known_width * focal_Length) / per_width
def process_frames():
    for frame in receive_frames():
        classLabelIDs, confidences, bboxs = net.detect(frame, confThreshold=0.4)

        bboxs = list(bboxs)
        confidences = list(np.array(confidences).reshape(1,-1)[0])
        confidences = list(map(float, confidences))

        bboxIdx = cv2.dnn.NMSBoxes(bboxs, confidences, score_threshold=0.55, nms_threshold=0.2)

        current_time = time.time()

        if len(bboxIdx) != 0:
            for i in range(0, len(bboxIdx)):
                bbox = bboxs[np.squeeze(bboxIdx[i])]
                classConfidence = confidences[np.squeeze(bboxIdx[i])]
                classLabelID = np.squeeze(classLabelIDs[np.squeeze(bboxIdx[i])])
                classLabel = classesList[classLabelID]

                classColor = [int(c) for c in colorList[classLabelID]]

                displayText = "{}:{:.2f}".format(classLabel, classConfidence)

                x, y, w, h = bbox

                if classLabel in KNOWN_WIDTHS:
                    width = w
                    distance = distance_to_camera(KNOWN_WIDTHS[classLabel], width, focal_Length=focal_length)
                    distance_text = "Distance: {:.2f}m".format(distance)
                    if distance < 1:
                        if classLabelID not in objects_within_distance:
                            objects_within_distance[classLabelID] = current_time
                            print(f"New object detected: {classLabel}")
                            generting_alert(f"alert from {classLabel}") # added this for web scoket
                        else:
                            if current_time - objects_within_distance[classLabelID] >= 1:
                                objects_within_distance[classLabelID] = current_time
                    else:
                        if classLabelID in objects_within_distance:
                            del objects_within_distance[classLabelID]
                else:
                    distance_text = "Distance: Unknown"

                cv2.rectangle(frame, (x, y), (x + w, y + h), color=classColor, thickness=1)
                cv2.putText(frame, displayText, (x, y - 10), cv2.FONT_HERSHEY_PLAIN, 1, classColor, 2)
                cv2.putText(frame, distance_text, (x, y + h + 20), cv2.FONT_HERSHEY_PLAIN, 1, classColor, 2)
            
            ret, buffer = cv2.imencode('.jpg',frame)
            binary = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + binary + b'\r\n') 



