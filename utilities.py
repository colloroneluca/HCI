from RecognitionClass import FaceRecognition
import time
from playsound import playsound
from micro import microphone
import threading
import time
from tkinter import *
import os
from PIL import Image, ImageTk
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
        if user is None:
            app.showErrorNoFaceDetected()
            time.sleep(5)
        elif user["username"] == "Unknown":
            response = app.signIn()
            if response == 1:
                user = app.addNewUser()
                break
            elif response == 2:
                # non vuole registrarsi
                print()
                break
            app.showInfoNewAttempt()
            time.sleep(3)
        else:
            print("welcome back ", str(user["username"]), "!!!")
            break
    return user

def getGesturesHelp():
    # Create an instance of tkinter frame
    win = Tk()
    win.overrideredirect(1)
    win.attributes('-topmost', 'true')

    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()

    # Set the Geometry
    win.geometry("100x30+{}+{}".format(screen_width - 100, 120))

    def toggle():
        if win.winfo_height() == 30:
            win.geometry("100x780+{}+{}".format(screen_width - 100, 120))
            button.config(bg='#333333')
            button.config(fg='#ffffff')
        else:
            win.geometry("100x30+{}+{}".format(screen_width - 100, 120))
            button.config(fg='#333333')
            button.config(bg='#ffffff')

    # Create a Button for toggle function
    button = Button(win, text="GESTURES", height=1, command=toggle)
    button.config(font=('Verdana', 7))
    button.config(fg='#333333')
    button.config(bg='#ffffff')
    button.config(activebackground='#7a7979')

    button.config(compound='bottom')
    button.pack(fill=X)

    path = 'GesturesImages'
    images_list = os.listdir(path)

    image_size = (100, 120)

    image = Image.open(path + '/' + images_list[0])
    image = image.resize(image_size)
    img1 = ImageTk.PhotoImage(image)
    label = Label(win, image=img1)
    label.pack()

    image = Image.open(path + '/' + images_list[1])
    image = image.resize(image_size)
    img2 = ImageTk.PhotoImage(image)
    label = Label(win, image=img2)
    label.pack()

    image = Image.open(path + '/' + images_list[2])
    image = image.resize(image_size)
    img3 = ImageTk.PhotoImage(image)
    label = Label(win, image=img3)
    label.pack()

    image = Image.open(path + '/' + images_list[3])
    image = image.resize(image_size)
    img4 = ImageTk.PhotoImage(image)
    label = Label(win, image=img4)
    label.pack()

    image = Image.open(path + '/' + images_list[4])
    image = image.resize(image_size)
    img5 = ImageTk.PhotoImage(image)
    label = Label(win, image=img5)
    label.pack()

    image = Image.open(path + '/' + images_list[5])
    image = image.resize(image_size)
    img6 = ImageTk.PhotoImage(image)
    label = Label(win, image=img6)
    label.pack()

    win.mainloop()