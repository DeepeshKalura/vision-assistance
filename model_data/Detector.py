import cv2
import numpy as np
import requests
import threading

np.random.seed(20)

class Detector:
    def __init__(self, server_address, configPath, modelPath, classesPath):
        self.server_address = server_address
        self.configPath = configPath
        self.modelPath = modelPath
        self.classesPath = classesPath

        self.net = cv2.dnn_DetectionModel(self.modelPath, self.configPath)
        self.net.setInputSize(320,320)
        self.net.setInputScale(1.0/127.5)
        self.net.setInputMean((127.5, 127.5, 127.5))
        self.net.setInputSwapRB(True)

        self.readClasses()
        self.known_width = 10
        self.focal_length = 280
        self.stop_event = threading.Event()

    def readClasses(self):
        with open(self.classesPath, 'r') as f:
            self.classesList = f.read().splitlines()

        self.classesList.insert(0, '__Background__')
        self.colorList = np.random.uniform(low=0, high=255, size=(len(self.classesList),3))

    def calculate_distance(self, known_width, focal_length, per_width):
        return (known_width * focal_length) / per_width

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

    def process_frames(self):
        for frame in self.receive_frames():
            classLabelIDs, confidences, bboxs = self.net.detect(frame, confThreshold=0.4)

            bboxs = list(bboxs)
            confidences = list(np.array(confidences).reshape(1,-1)[0])
            confidences = list(map(float, confidences))

            bboxIdx = cv2.dnn.NMSBoxes(bboxs, confidences, score_threshold=0.5, nms_threshold=0.2)

            if len(bboxIdx) != 0:
                for i in range(0, len(bboxIdx)):
                    bbox = bboxs[np.squeeze(bboxIdx[i])]
                    classConfidence = confidences[np.squeeze(bboxIdx[i])]
                    classLabelID = np.squeeze(classLabelIDs[np.squeeze(bboxIdx[i])])
                    classLabel = self.classesList[classLabelID]

                    classColor = [int(c) for c in self.colorList[classLabelID]]

                    displayText = "{}:{:.2f}".format(classLabel, classConfidence)

                    x, y, w, h = bbox

                    cv2.rectangle(frame, (x, y), (x + w, y + h), color=classColor, thickness=1)
                    cv2.putText(frame, displayText, (x, y - 10), cv2.FONT_HERSHEY_PLAIN, 1, classColor, 2)

                    object_width = w
                    distance = self.calculate_distance(known_width=10, focal_length=self.focal_length, per_width=object_width)
                    cv2.putText(frame, f"Distance: {distance:.2f} cm", (x, y + h + 20), cv2.FONT_HERSHEY_PLAIN, 1, classColor, 2)

            cv2.imshow("Result", frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord("q") or self.stop_event.is_set():
                break

        cv2.destroyAllWindows()

    def start_processing(self):
        threading.Thread(target=self.process_frames, daemon=True).start()

    def stop_processing(self):
        self.stop_event.set()
