import cv2
import numpy as np
import HandTrackingModule as htm
import time
import autopy
import cv2
import json
import mediapipe as mp
import time
import numpy as np
from os.path import exists
#from FaceRecognitionApp import FaceRecognizer
import cv2
import numpy as np
from PIL import Image
import os
import time
import json
import cv2
import numpy as np
import HandTrackingModule as htm
import time
import autopy
from selenium_browser import Selenium_Browser


def launch_face_recognizer():
    pass

class hand_gesture_browser():
    def __init__(self, cap, detector):
       self.container = [0,0,0,0,0]
       self.main(cap,detector)


    def get_click(self, fingers, img):
        if fingers[0] == 1 and fingers[1] == 1:
            # 9. Find distance between fingers
            length, img, lineInfo = detector.findDistance(8, 4, img)
            print(length)
            print("length", length)
            if length < 30:
                cv2.circle(img, (lineInfo[4], lineInfo[5]),
                           15, (0, 255, 0), cv2.FILLED)
                autopy.mouse.click()

    def get_mouse_movement(self, fingers, img, frameR, wCam, hCam, wScr, hScr, smoothening, plocX, plocY, x1,y1):
        if fingers[1] == 1 and fingers[2] == 0:
            # 5. Convert Coordinates
            x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))
            # 6. Smoothen Values
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening
            # 7. Move Mouse
            autopy.mouse.move(wScr - clocX, clocY)
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            plocX, plocY = clocX, clocY
        return plocX, plocY

    def get_movement(self, lmList, fingers, acquired):
        if fingers == [1,1,1,1,1]:
            self.container.insert(0,lmList[8][1])
        else:
            self.container.insert(0, None)
        if len(self.container)>5:
            self.container = self.container[:-1]
        print("container", self.container)
        difference = 0
        if len(self.container)>4:
            if None not in self.container:
                for i in range(len(self.container)-1):
                    difference += self.container[i] - self.container[i+1]
            else:
                difference = None
        if difference != None:
            if difference > 60:
                print("\nRIGHT\n")
                return("right2left")
            if difference < -60:
                print("\nLeft\n")
                return ("left2right")
        else:
            return None

    def main(self, cap, detector):
        ##########################
        wCam, hCam = 640, 480
        frameR = 100  # Frame Reduction
        smoothening = 7
        pTime = 0
        plocX, plocY = 0, 0
        clocX, clocY = 0, 0
        cap.set(3, wCam)
        cap.set(4, hCam)
        wScr, hScr = autopy.screen.size()
        acquired = False
        recovered = True
        time_since_tab_switch = time.time()
        b = Selenium_Browser()
        b.launch_browser()
        b.open_tab('https://www.google.com/')
        b.open_tab('https://www.youtube.com/')

        # print(wScr, hScr)

        ############################

        #############################
        #Main Loop
        #############################
        while True:
            # 1. Find hand Landmarks
            success, img = cap.read()
            img = detector.findHands(img)
            lmList, bbox = detector.findPosition(img)
            # 2. Get the tip of the index and middle fingers
            if len(lmList) != 0:
                x1, y1 = lmList[8][1:]
                x2, y2 = lmList[12][1:]
                fingers = detector.fingersUp()

                cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR),
                              (255, 0, 255), 2)

                movement = self.get_movement(lmList,fingers,acquired)
                if time.time()-time_since_tab_switch > 3 and recovered==False:
                    recovered = True
                if movement != None and recovered:
                    b.switch_to_tab(movement)
                    time_since_tab_switch = time.time()
                plocX, plocY = self.get_mouse_movement(fingers, img, frameR, wCam, hCam, wScr, hScr,
                                                       smoothening, plocX, plocY, x1,y1)
                self.get_click(fingers, img)

            # 11. Frame Rate
            cTime = time.time()
            fps = 1 / (cTime - pTime)
            pTime = cTime
            cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                        (255, 0, 0), 3)
            img = cv2.flip(img, 1)
            # 12. Display
            cv2.imshow("Image", img)
            cv2.waitKey(1)


if __name__=='__main__':
    cap = cv2.VideoCapture(2)
    detector = htm.handDetector(maxHands=1)
    v = hand_gesture_browser(cap, detector)