import os
import time
import pyautogui
import subprocess
import speech_recognition as sr


from app.utility import generate_audio
from app.multimodel import multimodel, encode_image
from app.sos import help_sms


r = sr.Recognizer()
global number

def stopingAll():
    pass

def start():
    global cv_process
    print("Starting the system...")
    streamlit_process = subprocess.Popen(["streamlit", "run", "web.py"])


def close():
    global streamlit_process
    print("Closing the system...")
    pyautogui.hotkey('alt', 'tab')
    if streamlit_process:
        streamlit_process.kill()


def scroll():
    print("Scrolling the page...")
    pyautogui.scroll(-100)


def switch():
    print("Switching the page...")
    pyautogui.hotkey('alt', 'tab')


def remove():
    pyautogui.hotkey('ctrl', 'w')
    print("removing the page..")


def explain_project():
    print("Explaining the project...")
    pyautogui.hotkey('alt', 'tab')
    pyautogui.hotkey('ctrl', 't')
    pyautogui.write("https://github.com/DeepeshKalura/vision-assistance")
    pyautogui.press('enter')
    time.sleep(0.2)
    
    

def main():
    global number
    number = 0 
    while True:
        number += 1
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

                if "describe" in text.lower():
                    print("describe keyword detected. Stopping streaming...")
                    # code written by saniya 
                    result = (multimodel(encode_image("./images/char.jpeg")))
                    generate_audio(result, str(number))
                    

                if "help" in text.lower():
                    print("help keyword detected. Stopping streaming...")
                    isreached = help_sms()
                    if isreached:
                        generate_audio("Help has been send to your location?")
                    else:
                        generate_audio("Failed to send help to your location. Please waiting help been sending.")

                

        
        except sr.UnknownValueError:
            print("Could not understand audio")
        


if __name__ == "__main__":
    main()
