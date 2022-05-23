import json
import cv2
import numpy as np
import face_recognition
import os
import time
from collections import Counter
import copy

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

        cap = cv2.VideoCapture(0)
        t_end = time.time() + 5
        prediction_list = []
        while time.time() < t_end:
            success, img = cap.read()
            imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
            imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

            facesCurFrame = face_recognition.face_locations(imgS)
            encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

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
        # set the new user infos
        username = input('\n enter username ==>  ')

        dominant_hand = input('\n enter your dominant hand (sx, dx) ==>  ')

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

        return {'id': int(last_id + 1), 'username': username, 'dominant_hand': dominant_hand, 'tabs': []}

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


#app = FaceRecognition()

'''images = app.getClassesImages()

app.saveEncodings(app.findEncodings(images))'''














