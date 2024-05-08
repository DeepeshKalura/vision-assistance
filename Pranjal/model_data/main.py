from Detector import *
import os

def main():
    videoPath = 0
    #For other videos change this ..^.. address.
    #For webcam , replace video path address with '0'. 

    configPath = os.path.join("model_data", "ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt")
    modelPath = os.path.join("model_data", "frozen_inference_graph.pb")
    classesPath = os.path.join("model_data", "coco.names")
    
    ### THIS IS FOR MY SYSTEM ###
     
    # configPath = "ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
    # modelPath = "frozen_inference_graph.pb"
    # classesPath = "coco.names"

    detector = Detector(videoPath, configPath, modelPath, classesPath)
    detector.onVideo()

if __name__ =='__main__':
    main()