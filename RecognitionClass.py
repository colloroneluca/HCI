import json
from tkinter import messagebox

import cv2
import numpy as np
import face_recognition
import os
import time
from collections import Counter
import copy
import tkinter as tk
from tkinter import *

class FaceRecognition:

    def __init__(self):
        self.class_names = []
        self.usersPath = 'users.json'
        self.path = 'ImagesAttendance'
        self.getClassesImages()
        self.encodeListKnown = self.getEncodings()
        self.users = self.getUsersList()

    def getClassesImages(self):
        imgs = []
        classes = []
        file_list = os.listdir(self.path)
        file_list.sort()
        print("Class Detected: ", file_list)
        for cl in file_list:
            cur_img = cv2.imread(f'{self.path}/{cl}')
            imgs.append(cur_img)
            classes.append(os.path.splitext(cl)[0])
        self.class_names = classes
        print("Num classes ", len(self.class_names))
        return imgs

    def findEncodings(self, images):
        encodeList = []
        for index, img in enumerate(images):
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            result = face_recognition.face_encodings(img)
            if result:
                encode = result[0]
                encodeList.append(encode.tolist())
            else:
                os.remove('ImagesAttendance/' + self.class_names[index] + '.png')
                print(self.class_names[index])
                self.class_names.pop(index)
        print("Encodings completed")
        return encodeList

    def saveEncodings(self, encodeList):
        with open('encodings.json', 'w') as outfile:
            json.dump(encodeList, outfile)
        print("Encoding saved")

    def getEncodings(self):
        with open('encodings.json', 'r+') as f:
            encodeList = json.load(f)
        print("Num encodings ", len(encodeList))
        return encodeList

    def recognition(self):
        if len(self.encodeListKnown) == 0:
            cap = cv2.VideoCapture(0)
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            t_end = time.time() + 5
            while time.time() < t_end:
                success, img = cap.read()
                imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
                imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

                facesCurFrame = face_recognition.face_locations(imgS)
                encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)
                if facesCurFrame:
                    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):

                        name = "Unknown"

                        y1, x2, y2, x1 = faceLoc
                        y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                        cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 1)
                else:
                    cv2.putText(img, "Stay in front the camera", (55, 240), cv2.FONT_HERSHEY_DUPLEX, 1.3, (0, 0, 255),2)
                cv2.imshow('Webcam', img)
                cv2.waitKey(1)
            cap.release()
            cv2.destroyAllWindows()
            return self.getUserFromUsername('Unknown')

        else:
            cap = cv2.VideoCapture(0)
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            t_end = time.time() + 5
            prediction_list = []
            while time.time() < t_end:
                success, img = cap.read()
                imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
                imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

                facesCurFrame = face_recognition.face_locations(imgS)
                encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)
                if facesCurFrame:
                    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
                        matches = face_recognition.compare_faces(self.encodeListKnown, encodeFace)
                        faceDis = face_recognition.face_distance(self.encodeListKnown, encodeFace)
                        matchIndex = np.argmin(faceDis)

                        if faceDis[matchIndex] < 0.5:
                            userIndex = self.class_names[matchIndex].split(".")[1]
                            name = self.users[int(userIndex)]['username']
                        else:
                            name = "Unknown"

                        prediction_list.append(name)

                        y1, x2, y2, x1 = faceLoc
                        y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                        cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 1)
                else:
                    cv2.putText(img, "Stay in front the camera", (55, 240), cv2.FONT_HERSHEY_DUPLEX, 1.3, (0, 0, 255), 2)

                cv2.imshow('Webcam', img)
                cv2.waitKey(1)

            cap.release()
            cv2.destroyAllWindows()

            c = Counter(prediction_list)
            if prediction_list:
                username = c.most_common(1)[0][0]
            else:
                username = "None"
            return self.getUserFromUsername(username)

    def addNewUser(self):

        # Define the detector
        detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        # get the last id
        last_id = self.users[-1]['id']

        username, dominant_hand = self.signIn()

        self.saveNewUser(last_id + 1, username, dominant_hand)

        cam = cv2.VideoCapture(0)
        img_counter = 0
        images = []
        count = 0
        while True:
            ret, frame = cam.read()
            if not ret:
                print("failed to grab frame")
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(
                gray,
                scaleFactor=1.2,
                minNeighbors=5,
                minSize=(30, 30)
            )
            pic = copy.copy(frame)
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 1)

            cv2.imshow("Registration - Please press SPACE to take picture", frame)

            k = cv2.waitKey(1)
            if k % 256 == 27:
                # ESC pressed
                print("Escape hit, closing...")
                break
            elif k % 256 == 32:
                # SPACE pressed
                count += 1
                img_name = 'ImagesAttendance/User.' + str(last_id + 1) + '.' + str(count) + ".png"
                cv2.imwrite(img_name, pic)
                images.append(pic)
                print("{} written!".format(img_name))
                img_counter += 1
        cam.release()
        cv2.destroyAllWindows()

        # Update classes list with the new pics saved
        self.getClassesImages()
        for x in self.findEncodings(images):
            self.encodeListKnown.append(x)
        self.saveEncodings(self.encodeListKnown)

        return {'id': int(last_id + 1), 'username': username, 'dominant': dominant_hand, 'tabs': []}

    def saveNewUser(self, face_id, username, dominant_hand):
        self.users.append({'id': int(face_id), 'username': username, 'dominant_hand': dominant_hand, 'tabs': []})
        with open(self.usersPath, 'w') as f:
            json.dump(self.users, f, indent=4, separators=(',', ': '))

    def getUsersList(self):
        with open(self.usersPath, 'r+') as f:
            users = json.load(f)
        return users

    def getUserFromUsername(self, username):
        for user in self.users:
            if user["username"] == username:
                return user

    def signIn(self):
        root = Tk()
        root.title("Registration Form")
        root.resizable(False, False)  # This code helps to disable windows from resizing
        root.attributes('-topmost', 'true')

        window_height = 420
        window_width = 640

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        x_cordinate = int((screen_width / 2) - (window_width / 2))
        y_cordinate = int((screen_height / 2) - (window_height / 2))

        root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

        username = StringVar()
        dominant_hand = StringVar()

        def check():
            if str(entry_1.get()) != '' and str(entry_2.get()) == "Right" or str(entry_2.get()) == "Left":
                root.destroy()
            else:
                messagebox.showerror("Error", "Please enter the data in the correct format (Left, Right)")

        label_0 = Label(root, text="Registration form", font=("bold", 20))
        label_0.pack(side=TOP, pady=10)

        label_1 = Label(root, text="Username", font=("bold", 12))
        label_1.pack(side=TOP, ipady=10)

        entry_1 = Entry(root, textvariable=username)
        entry_1.pack(side=TOP, ipady=5,  pady=5)

        label_2 = Label(root, text="Dominant hand (Left, Right)", font=("bold", 12))
        label_2.pack(side=TOP, ipady=10)

        entry_2 = Entry(root, textvariable=dominant_hand)
        entry_2.pack(side=TOP, ipady=5, pady=5)

        Button(root, text='Submit', width=20, bg='brown', fg='white', command=check).pack(side=TOP, pady=10)

        root.mainloop()
        return str(username.get()), str(dominant_hand.get())

    def showErrorNoFaceDetected(self):
        Tk().withdraw()
        messagebox.showerror("Error", "Please stay in front the camera. Press ok and wait a few seconds and try again")
        return

    def showInfoNewAttempt(self):
        Tk().withdraw()
        messagebox.showinfo("New Attempt", "Press ok and wait a few seconds and the camera will start again")
        return

    def askRegistration(self):
        root = Tk()
        root.attributes('-topmost', 'true')

        var = IntVar()

        def sel():
            print(var.get())
            if str(var.get()) in ["1", "2", "3"]:
                root.destroy()
            else:
                messagebox.showerror("Error", "Please select an option")

        window_height = 420
        window_width = 640

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        x_cordinate = int((screen_width / 2) - (window_width / 2))
        y_cordinate = int((screen_height / 2) - (window_height / 2))

        root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

        label_0 = Label(root,
                        text="Seems it is the first time you use this application \n "
                             "do you want to register?",
                        font=("bold", 15))
        label_0.pack(side=TOP, ipady=10)

        # Dictionary to create multiple buttons
        values = {"YES  ": "1",
                  "NO   ": "2",
                  "RETRY": "3"}
        # Loop is used to create multiple Radiobuttons
        # rather than creating each button separately
        for (text, value) in values.items():
            Radiobutton(root, text=text, variable=var,
                        value=value).pack(side=TOP, ipady=5)

        Button(root, text='Submit', width=20, bg='brown', fg='white', command=sel).pack(side=TOP, pady=10)

        label = Label(root)
        label.pack()

        root.mainloop()

        return var.get()











