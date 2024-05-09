import os
from model_data.Detector import *



server_address = "http://192.168.137.235/"
configPath = "/model_data/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
modelPath = "/model_data/frozen_inference_graph.pb"
classesPath = "/model_data/coco.names"


detector = Detector(server_address, configPath, modelPath, classesPath)
def server_start():
    detector.start_processing()
   

def object_detection():
    detector.start_processing()


