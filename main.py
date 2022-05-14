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
import pyautogui
from os.path import exists
from RecognitionClass import FaceRecognition
from keyboard import keyboard
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

class hand_gesture_browser():
    def __init__(self, cap, detector):
       self.container = [0,0,0,0,0]
       self.last_click_time = 0
       self.clicked = False
       self.main(cap,detector)


    def get_scroll(self, img, lmlist, wCam, hCam):

        length, img, lineInfo = detector.findDistance(8, 12, img)
        if length < 50:
            cv2.line(img, (0, hCam//2), (wCam, hCam//2), (0, 255, 0), 2)
            cv2.line(img, (0, hCam//4), (wCam, hCam//4), (255, 0, 0), 2)
            cv2.line(img, (0, (hCam//2) + (hCam//4)), (wCam, (hCam//2) + (hCam//4)), (255, 0, 0), 2)

            if lmlist[8][2] < hCam // 4:
                pyautogui.scroll(120)
            elif hCam//4 < lmlist[8][2] < hCam//2:
                pyautogui.scroll(80)
            elif hCam//2 < lmlist[8][2] < hCam//2 + hCam//4:
                pyautogui.scroll(-80)
            else:
                pyautogui.scroll(120)


    def get_hold_click(self, fingers, img, frameR, wCam, hCam, wScr, hScr, smoothening, plocX, plocY, x13, y13, x1, y1):

        # 5. Convert Coordinates
        x3 = np.interp(x13, (frameR, wCam - frameR), (0, wScr))
        y3 = np.interp(y13, (frameR, hCam - frameR), (0, hScr))
        # 6. Smoothen Values
        clocX = plocX + (x3 - plocX) / smoothening
        clocY = plocY + (y3 - plocY) / smoothening
        pyautogui.mouseDown()
        # 7. Move Mouse
        autopy.mouse.move(wScr - clocX, clocY)
        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        plocX, plocY = clocX, clocY


        return plocX, plocY

    def get_click(self, fingers, img):

        # 9. Find distance between fingers
        length, img, lineInfo = detector.findDistance(8, 4, img)
        print("Distance between click fingers:", length)

        #if self.clicked == True:
        if length < 50 and time.time() - self.last_click_time > 1.5:
            self.last_click_time = time.time()
            cv2.circle(img, (lineInfo[4], lineInfo[5]),
                       15, (0, 255, 0), cv2.FILLED)
            autopy.mouse.click()

        """if length < 50:
            self.clicked = True
        else:
            self.clicked = False
        """
    def get_mouse_movement(self, fingers, img, frameR, wCam, hCam, wScr, hScr, smoothening, plocX, plocY, x13,y13, x1,y1):

        # 5. Convert Coordinates
        x3 = np.interp(x13, (frameR, wCam - frameR), (0, wScr))
        y3 = np.interp(y13, (frameR, hCam - frameR), (0, hScr))
        # 6. Smoothen Values
        clocX = plocX + (x3 - plocX) / smoothening
        clocY = plocY + (y3 - plocY) / smoothening
        # 7. Move Mouse
        autopy.mouse.move(wScr - clocX, clocY)
        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        plocX, plocY = clocX, clocY
        return plocX, plocY

    def get_movement(self, lmList, fingers, acquired):
        if sum(fingers) >= 4:
            self.container.insert(0,lmList[8][1])
        else:
            self.container.insert(0, None)
        if len(self.container)>10:
            self.container = self.container[:-1]
        #print("container", self.container)
        difference = 0
        if len(self.container)>4:
            if None not in self.container:
                for i in range(len(self.container)-1):
                    difference += self.container[i] - self.container[i+1]
            else:
                difference = None
        if difference != None:
            print("Difference =>", difference)
            if difference > 60:
                print("\nRIGHT\n")
                return ("right2left")
            if difference < -60:
                print("\nLeft\n")
                return ("left2right")
        else:
            return None

    def main(self, cap, detector):
        ##########################
        wCam, hCam = 640, 480
        frameR = 80  # Frame Reduction
        smoothening = 7
        pTime = 0
        plocX, plocY = 0, 0
        clocX, clocY = 0, 0
        cap.set(3, wCam)
        cap.set(4, hCam)
        wScr, hScr = autopy.screen.size()
        acquired = False
        recovered = True
        time_to_wait_after_tab_switch = 1.5
        time_since_tab_switch = time.time()
        b = Selenium_Browser()
        b.launch_browser()
        b.open_tab('https://www.google.com/')
        b.open_tab('https://www.youtube.com/')
        time.sleep(1)
        b.script()
        ##############################
        keyboard = True
        if keyboard:
            k = KeyboardThread()
            k.start()
        #############################
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
                x13, y13 = lmList[13][1:]
                x2, y2 = lmList[12][1:]
                fingers = detector.fingersUp()

                cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR),
                              (255, 0, 255), 2)

                movement = self.get_movement(lmList,fingers,acquired)

                ###############################MOVE######################################
                if time.time()-time_since_tab_switch > time_to_wait_after_tab_switch:
                    recovered = True
                if movement != None and recovered:
                    b.switch_to_tab(movement)
                    time_since_tab_switch = time.time()
                    recovered = False
                ###########################################################################

                if fingers == [0, 1, 1, 0, 0]:
                    self.get_scroll(img, lmList, wCam, hCam)

                elif fingers[0] == 1 and fingers[1] == 1:
                    self.get_click(fingers, img)
                elif fingers != [1,1,1,1,1] and fingers !=[0,0,0,0,0]:
                    plocX, plocY = self.get_mouse_movement(fingers, img, frameR, wCam, hCam, wScr, hScr,
                                                           smoothening, plocX, plocY, x13,y13-50, x1,y1)
                """"elif fingers == [0,0,0,0,0]:
                    plocX, plocY = self.get_hold_click(fingers, img, frameR, wCam, hCam, wScr, hScr,
                    
                                                       smoothening, plocX, plocY, x1, y1)
                else:
                    pyautogui.mouseUp()
                """


            # 11. Frame Rate
            cTime = time.time()
            fps = 1 / (cTime - pTime)
            pTime = cTime
            img = cv2.flip(img, 1)
            cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                        (255, 0, 0), 3)
            # 12. Display
            cv2.imshow("Image", img)
            cv2.waitKey(1)

def start_recognition():
    app = FaceRecognition()
    while True:

        # 1. Get all the available classes
        classes, images = app.getClassesImages()

        # 2. Apply the recognition
        user = app.recognition(classes)

        # app.saveEncodings(app.findEncodings(images))
        # break

        # 3. Check if the user is registered
        if user == "Unknown":
            response = input("Seems it is the first time you use this application, do you want to register? (y/n)")
            if response == "y":
                app.addNewUser()
            break
        else:
            print("welcome back ", str(user), "!!!")
            break

import threading

class KeyboardThread (threading.Thread):
   def __init__(self):
      threading.Thread.__init__(self)

   def run(self):
      k = keyboard()


if __name__=='__main__':
    use_face_recognition = False
    if use_face_recognition:
        start_recognition()
    cap = cv2.VideoCapture(0)
    print("CAP", cap)
    detector = htm.handDetector(maxHands=1)
    v = hand_gesture_browser(cap, detector)
