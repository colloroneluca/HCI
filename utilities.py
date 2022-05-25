from RecognitionClass import FaceRecognition
import time
from playsound import playsound
from micro import microphone
import threading
import time

import pygame


def play(sound_, vol):
    sound = pygame.mixer.Sound(sound_)
    sound.set_volume(vol)
    sound.play()

def start_sound(sound, vol=1):

    x = threading.Thread(target=play, args=(sound,vol))
    x.start()



def start_micro(lista):
    m = microphone()
    lista.append(m)
    return lista

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