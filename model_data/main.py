from Detector import *
import os

def main():
    server_address = "http://192.168.1.1"

    configPath = os.path.join("model_data", "ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt")
    modelPath = os.path.join("model_data", "frozen_inference_graph.pb")
    classesPath = os.path.join("model_data", "coco.names")

    detector = Detector(server_address, configPath, modelPath, classesPath)
    detector.start_processing()

    input("Press Enter to stop processing...")

    detector.stop_processing()

if __name__ =='__main__':
    main()
