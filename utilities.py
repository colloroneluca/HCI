from RecognitionClass import FaceRecognition
import time
from playsound import playsound

import threading
import time

def play(sound_):

    playsound(sound_)

def start_sound(sound):

    x = threading.Thread(target=play, args=(sound,))
    x.start()


def background_startup(detector, cap):
    counter = 0
    while counter < 50:
        print(detector.counter)
        success, img = cap.read()
        img = detector.findHands(img)
        lmList, current_hand, counter = detector.findPosition(img)

def start_recognition():
    app = FaceRecognition()
    while True:
        # 1. Get all the available classes
        #classes, images = app.getClassesImages()

        # 2. Apply the recognition
        user = app.recognition()

        # 3. Check if the user is registered
        if user["username"] == "Unknown":
            response = input("Seems it is the first time you use this application, do you want to register? (y/n)")
            if response == "y":
                user = app.addNewUser()
            else:
                # run as default user or exit
                print()
            break
        elif user["username"] == "None":
            print("Please stay in front the camera!!")
            time.sleep(5)
        else:
            print("welcome back ", str(user["username"]), "!!!")
            break
    return user