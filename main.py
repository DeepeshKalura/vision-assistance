import os
import subprocess
import speech_recognition as sr
from app.audio import generate_audio
from app.multimodel import multimodel, encode_image
import streamlit as st
import pyautogui

r = sr.Recognizer()


def stopingAll():
    pass

def start():
    global streamlit_process
    print("Starting the system...")
    streamlit_process = subprocess.Popen(["streamlit", "run", "web.py"])


def close():
    global streamlit_process
    print("Closing the system...")
    pyautogui.hotkey('alt', 'tab')
    if streamlit_process:
        streamlit_process.kill()
    
    

def main():
    while True:
        try:
            with sr.Microphone() as mic:
                print("Say something!")
                audio = r.listen(source=mic, phrase_time_limit=2 ) # Time out is giving
                result = r.recognize_azure(audio_data=audio, key=os.getenv("AZURE_API_KEY"), language='en-US', location="eastus", profanity="masked")
                print(result)
                text = result[0]
                print(type(text), type(result))
                print(text)
                print("You said:", text)

                if "start" in text.lower():
                    print("Start keyword detected. Starting the system...")
                    start()
                

                if "close" in text.lower():
                    print("Close keyword detected. Stopping streaming...")
                    close()
        
                


                if "stop" in text.lower():
                    print("Stop keyword detected. Stopping streaming...")
                    stopingAll()
                    break

                
                # hit point logic issue hai
                if "describe" in text.lower():
                    print("describe keyword detected. Stopping streaming...")
                    # code run saniya 
                    result = (multimodel(encode_image("./images/char.jpeg")))
                    generate_audio(result)
                    

                if "help" in text.lower():
                    print("help keyword detected. Stopping streaming...")
                    generate_audio("Help has been send to your location?")
                    
                
                if "talk" in text.lower():
                    print("help keyword detected. Stopping streaming...")
                    generate_audio("Talk to me")
                    

        
        except sr.UnknownValueError:
            print("Could not understand audio")
        


if __name__ == "__main__":
    main()

