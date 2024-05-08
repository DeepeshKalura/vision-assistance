import cv2
import numpy as np
import time
import streamlit as st

np.random.seed(20)

class Detector:
    def __init__(self, videoPath, configPath, modelPath, classesPath):
        self.videoPath = videoPath
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

    def readClasses(self):
        with open(self.classesPath, 'r') as f:
            self.classesList = f.read().splitlines()

        self.classesList.insert(0, '__Background__')
        self.colorList = np.random.uniform(low=0, high=255, size=(len(self.classesList),3))

    def calculate_distance(self, known_width, focal_length, per_width):
        return (known_width * focal_length) / per_width

    def onVideo(self):
        ### CODE CHANGES HERE ###
        st.title("Live Video Capture with OpenCV and Streamlit")
        framer = st.empty()
        ### CODE CHANGES HERE ###
        cap = cv2.VideoCapture(self.videoPath)

        if not cap.isOpened():
            print("Error Opening Video File...")
            return

        (success, image) = cap.read()

        while success:
            classLabelIDs, confidences, bboxs = self.net.detect(image, confThreshold = 0.4)

            bboxs = list(bboxs)
            confidences = list(np.array(confidences).reshape(1,-1)[0])
            confidences = list(map(float, confidences))

            bboxIdx = cv2.dnn.NMSBoxes(bboxs, confidences, score_threshold = 0.5, nms_threshold = 0.2)

            if len(bboxIdx) != 0:
                for i in range(0, len(bboxIdx)):
                    bbox = bboxs[np.squeeze(bboxIdx[i])]
                    classConfidence = confidences[np.squeeze(bboxIdx[i])]
                    classLabelID = np.squeeze(classLabelIDs[np.squeeze(bboxIdx[i])])
                    classLabel = self.classesList[classLabelID]

                    classColor = [int(c) for c in self.colorList[classLabelID]]

                    displayText = "{}:{:.2f}".format(classLabel, classConfidence)

                    x, y, w, h = bbox

                    cv2.rectangle(image, (x, y), (x + w, y + h), color=classColor, thickness=1)
                    cv2.putText(image, displayText, (x, y - 10), cv2.FONT_HERSHEY_PLAIN, 1, classColor, 2)

                    object_width = w
                    distance = self.calculate_distance(known_width=10, focal_length=self.focal_length, per_width=object_width)
                    cv2.putText(image, f"Distance: {distance:.2f} cm", (x, y + h + 20), cv2.FONT_HERSHEY_PLAIN, 1, classColor, 2)

            # cv2.imshow("Result", image)
            
            ### CODE CHANGES HERE ###
            image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
            framer.image(image, channels="RGB")
            ### CODE CHANGES HERE ###
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break

            (success, image) = cap.read()

        cv2.destroyAllWindows()
