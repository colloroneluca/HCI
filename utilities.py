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


class thread_with_exception(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self._stop_event = threading.Event()
        self.name = name
        self.destroyed = None
        self.win = None
        self.screen_width = None
        self.screen_height = None
        self.i = 0

    def run(self):

        # target function of the thread class
        try:
            print("STARTING", self.name)
            self.getGesturesHelp()
        finally:
            print('ended')
            while True:
                time.sleep(1)

    def get_id(self):

        # returns id of the respective thread
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id
    def my_join(self):
        print("about to join")
        self.join()
        print("joined")

    def stop(self):
        self._stop_event.set()

    def raise_exception(self):
        print("GETTING EXEption")
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,
                                                         ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print('Exception raise failure')
        print("done")

    def button_hover(self, e):
        self.win.geometry("100x750+{}+{}".format(self.screen_width - 100, 120))
        self.button.config(bg='#333333')
        self.button.config(fg='#ffffff')

    def button_leave(self, e):
        self.win.geometry("100x30+{}+{}".format(self.screen_width - 100, 120))
        self.button.config(fg='#333333')
        self.button.config(bg='#ffffff')

    def getGesturesHelp(self):
        print("in gesture")
        # Create an instance of tkinter frame
        self.win = None
        self.win = Tk()
        print("after tk")
        self.win.overrideredirect(1)
        self.win.attributes('-topmost', 'true')
        print("after tk2")
        self.screen_width = self.win.winfo_screenwidth()
        self.screen_height = self.win.winfo_screenheight()

        # Set the Geometry
        self.win.geometry("100x30+{}+{}".format(self.screen_width - 100, 120))

        print("after tk3")
        # Create a Button for toggle function
        self.button = Button(self.win, text="GESTURES", height=1)
        self.button.config(font=('Verdana', 7))
        self.button.config(fg='#333333')
        self.button.config(bg='#ffffff')
        self.button.config(activebackground='#7a7979')

        self.button.config(compound='bottom')
        self.button.pack(fill=X)

        self.button.bind("<Enter>", self.button_hover)
        self.button.bind("<Leave>", self.button_leave)

        path = 'GesturesImages'
        print("after tk4")
        images_list = os.listdir(path)

        image_size = (100, 120)
        print("after tk5")

        image = Image.open(path + '/' + images_list[0])
        print("after tk5a")
        image = image.resize(image_size)
        print("after tk5b")
        print(image)

        try:
            #img1 = ImageTk.PhotoImage(image=PIL.Image.fromarray(image))
            print("self.i", self.i)
            if self.i == 0:

                img1 = ImageTk.PhotoImage(image)
                self.img1 = img1
                print("correct")
        except:
            img1 = self.img1
            print("After")


        print("after tk5c")
        label = Label(self.win, image=img1)
        label.pack()
        print("after tk6")
        image = Image.open(path + '/' + images_list[1])
        image = image.resize(image_size)
        img2 = ImageTk.PhotoImage(image)
        image.close()
        label = Label(self.win, image=img2)
        label.pack()
        print("after tk7")
        image = Image.open(path + '/' + images_list[2])
        image = image.resize(image_size)
        img3 = ImageTk.PhotoImage(image)
        image.close()
        label = Label(self.win, image=img3)
        label.pack()

        image = Image.open(path + '/' + images_list[3])
        image = image.resize(image_size)
        img4 = ImageTk.PhotoImage(image)
        image.close()
        label = Label(self.win, image=img4)
        label.pack()

        image = Image.open(path + '/' + images_list[4])
        image = image.resize(image_size)
        img5 = ImageTk.PhotoImage(image)
        image.close()
        label = Label(self.win, image=img5)
        label.pack()

        image = Image.open(path + '/' + images_list[5])
        image = image.resize(image_size)
        img6 = ImageTk.PhotoImage(image)
        image.close()
        label = Label(self.win, image=img6)
        label.pack()
        self.i += 1
        print("before after")
        self.win.after(1000, self.check)
        print("BEFORE mainloop")

        self.win.mainloop()

    def check(self):

        if self.destroyed == True:
            self.destroyed = False
            self.win.destroy()
            time.sleep(1)
        else:

            self.win.after(1000, self.check)

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
            response = app.askRegistration()
            if response == 1:
                user = app.addNewUser()
                break
            elif response == 2:
                return {'id': None, 'username': 'GuestUser', 'dominant': 'Right', 'tabs': []}
            else:
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
