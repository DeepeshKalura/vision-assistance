import os
import subprocess
import speech_recognition as sr

from app.utility import generate_audio
from app.multimodel import multimodel
from app.sos import help_sms
from app.read import message

r = sr.Recognizer()


global number
global running

def start():
    global running
    running = subprocess.run(["python", "model_data/main.py"])


def stop():
    global running
    running.kill()

def main():
    global number
    number = 0 
    while True:
        number += 1
        try:
            with sr.Microphone() as mic:
                print("Say something!...") 
                audio = r.listen(source=mic, phrase_time_limit=2 ) # Time out is giving
                result = r.recognize_azure(audio_data=audio, key=os.getenv("AZURE_API_KEY"), language='en-US', location="eastus", profanity="masked")
                print(result)
                text = result[0]
                if "start" in text.lower():
                    start()

                if "stop" in text.lower():
                    print("Stop keyword detected. Stopping streaming...")
                    stop()
                    break

                if "describe" in text.lower():
                    print("describe keyword detected. Stopping streaming...")
                    # code written by saniya 
                    result = multimodel()
                    generate_audio(result, str(number)+".mp3+")
                    
                if "help" in text.lower():
                    print("help keyword detected. Stopping streaming...")
                    isreached = help_sms()
                    if isreached:
                        if(os.path.exists("audio/able_send_help.mp3") == False):
                            generate_audio("Help has been send to your location?", "able_send_help.mp3")
                    else:
                        if (os.path.exists("audio/unable_send_help.mp3") == False):
                            generate_audio("Failed to send help to your location. Please waiting help been sending.", "unable_send_help.mp3")

                if "read" in text.lower():
                    result = message()
                    if result:
                        if (not os.path.exists("audio/message.mp3")):
                            generate_audio(result, "audio/message.mp3")

                        
        except sr.UnknownValueError:
            print("Could not understand audio")

if __name__ == "__main__":
    main()
