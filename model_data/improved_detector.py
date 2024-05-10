import cv2
import numpy as np
import requests


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

def receive_frames():
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
                yield frame
                # yield (b'--frame\r\n'b'Content-Type: image/jpg\r\n\r\n' + frame + b'\r\n')


def process_frames():
        
        for frame in receive_frames():
            classLabelIDs, confidences, bboxs = net.detect(frame, confThreshold=0.4)

            bboxs = list(bboxs)
            confidences = list(np.array(confidences).reshape(1,-1)[0])
            confidences = list(map(float, confidences))

            bboxIdx = cv2.dnn.NMSBoxes(bboxs, confidences, score_threshold=0.5, nms_threshold=0.2)

            if len(bboxIdx) != 0:
                for i in range(0, len(bboxIdx)):
                    bbox = bboxs[np.squeeze(bboxIdx[i])]
                    classConfidence = confidences[np.squeeze(bboxIdx[i])]
                    classLabelID = np.squeeze(classLabelIDs[np.squeeze(bboxIdx[i])])
                    classLabel = classesList[classLabelID]

                    classColor = [int(c) for c in colorList[classLabelID]]

                    displayText = "{}:{:.2f}".format(classLabel, classConfidence)

                    x, y, w, h = bbox

                    cv2.rectangle(frame, (x, y), (x + w, y + h), color=classColor, thickness=1)
                    cv2.putText(frame, displayText, (x, y - 10), cv2.FONT_HERSHEY_PLAIN, 1, classColor, 2)

                    object_width = w
                    distance = calculate_distance(known_width=10, focal_length=focal_length, per_width=object_width)
                    cv2.putText(frame, f"Distance: {distance:.2f} cm", (x, y + h + 20), cv2.FONT_HERSHEY_PLAIN, 1, classColor, 2)
            
            ret, buffer = cv2.imencode('.jpg',frame)
            binary = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + binary + b'\r\n') 



