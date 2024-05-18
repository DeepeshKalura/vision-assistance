import cv2
import numpy as np
import threading
import time
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.utility import generate_audio, play_audio




np.random.seed(20)

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




class SimpleDetector:
    def __init__(self,  configPath, modelPath, classesPath, focalLength):
        self.configPath = configPath
        self.modelPath = modelPath
        self.classesPath = classesPath
        self.focalLength = focalLength
        self.processing = False

        self.net = cv2.dnn_DetectionModel(self.modelPath, self.configPath)
        self.net.setInputSize(320,320)
        self.net.setInputScale(1.0/127.5)
        self.net.setInputMean((127.5, 127.5, 127.5))
        self.net.setInputSwapRB(True)

        self.readClasses()

        self.objects_within_distance = {}  # Dictionary to store objects within distance

    def readClasses(self):
        with open(self.classesPath, 'r') as f:
            self.classesList = f.read().splitlines()

        self.classesList.insert(0, '__Background__')
        self.colorList = np.random.uniform(low=0, high=255, size=(len(self.classesList),3))


    def _process_song(self, text):
        generate_audio(name="alert.mp3", text=text)
        play_audio("alert.mp3")
        self.processing = False

    def new_process_song(self, text):
        if self.processing:
            pass
        else:
            self.processing = True
            thread = threading.Thread(target=self._process_song, args=(text,))
            thread.start()

    def distance_to_camera(self, known_width, per_width, focal_Length):
        return (known_width * focal_Length) / per_width

    
    def process_frames(self):
        cap = cv2.VideoCapture(0)  # Open default camera

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            classLabelIDs, confidences, bboxs = self.net.detect(frame, confThreshold=0.4)

            bboxs = list(bboxs)
            confidences = list(np.array(confidences).reshape(1, -1)[0])
            confidences = list(map(float, confidences))

            bboxIdx = cv2.dnn.NMSBoxes(bboxs, confidences, score_threshold=0.55, nms_threshold=0.2)

            current_time = time.time()

            if len(bboxIdx) != 0:
                for i in range(len(bboxIdx)):
                    bbox = bboxs[np.squeeze(bboxIdx[i])]
                    classConfidence = confidences[np.squeeze(bboxIdx[i])]
                    classLabelID = np.squeeze(classLabelIDs[np.squeeze(bboxIdx[i])])
                    classLabel = self.classesList[classLabelID]

                    classColor = [int(c) for c in self.colorList[classLabelID]]

                    displayText = "{}:{:.2f}".format(classLabel, classConfidence)

                    x, y, w, h = bbox

                    if classLabel in KNOWN_WIDTHS:
                        width = w
                        distance = self.distance_to_camera(KNOWN_WIDTHS[classLabel], width, self.focalLength)
                        distance_text = "Distance: {:.2f}m".format(distance)
                        if distance < 1:
                            if classLabelID not in self.objects_within_distance:
                                self.objects_within_distance[classLabelID] = current_time
                                print(f"New object detected: {classLabel}")
                                self.new_process_song(f"alert from {classLabel}")
                            else:
                                if current_time - self.objects_within_distance[classLabelID] >= 1:
                                    self.objects_within_distance[classLabelID] = current_time
                        else:
                            if classLabelID in self.objects_within_distance:
                                del self.objects_within_distance[classLabelID]
                    else:
                        distance_text = "Distance: Unknown"

                    cv2.rectangle(frame, (x, y), (x + w, y + h), color=classColor, thickness=1)
                    cv2.putText(frame, displayText, (x, y - 10), cv2.FONT_HERSHEY_PLAIN, 1, classColor, 2)
                    cv2.putText(frame, distance_text, (x, y + h + 20), cv2.FONT_HERSHEY_PLAIN, 1, classColor, 2)

            cv2.imshow("Result", frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord("q") :
                break

        cap.release()
        cv2.destroyAllWindows()
