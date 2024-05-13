import os
import subprocess
import speech_recognition as sr
import sys

from utility import generate_audio, play_audio
from sos import help_sms
from multimodel import message, describe_surrounding

r = sr.Recognizer()

# path = os.getcwd()
# sys.path.append(f'{path}/app')




def start():
    running = subprocess.run(["python", "model_data/main.py"])



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
                    print("Stop keyword detected. stopping streaming ")
                    break

                if "describe" in text.lower():
                    print("describe keyword detected. Stopping streaming...")
                    # code written by saniya 
                    result = describe_surrounding()
                    generate_audio(result, str(number)+".mp3")
                    play_audio(str(number)+".mp3")
                    
                if "help" in text.lower():
                    print("help keyword detected. Stopping streaming...")
                    isreached = help_sms()
                    if isreached:
                        if(os.path.exists("audio/able_send_help.mp3") == False):
                            generate_audio("Help has been send to your location?", "able_send_help.mp3")
                        play_audio("able_send_help.mp3")
                    else:
                        if (os.path.exists("audio/unable_send_help.mp3") == False):
                            generate_audio("Failed to send help to your location. Please waiting help been sending.", "unable_send_help.mp3")

                        play_audio("unable_send_help.mp3")

                if "read" in text.lower():
                    result = message()
                    generate_audio(result, str(number)+".mp3")
                    play_audio(str(number)+".mp3")

                        
        except sr.UnknownValueError:
            print("Could not understand audio")

if __name__ == "__main__":
    main()
