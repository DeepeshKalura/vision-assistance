import os

from for_pc_camera_detector import SimpleDetector

def main():
    configPath = os.path.join("model_data", "ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt")
    modelPath = os.path.join("model_data", "frozen_inference_graph.pb")
    classesPath = os.path.join("model_data", "coco.names")
    focalLength = 367 

    detector = SimpleDetector(configPath=configPath, modelPath=modelPath, classesPath=classesPath,focalLength= focalLength)
    detector.process_frames()



if __name__ == '__main__':
    main()
