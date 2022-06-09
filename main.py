#!/usr/bin/python3.8
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
import pygame
import selenium
from os.path import exists
from RecognitionClass import FaceRecognition
from keyboard import keyboard
from playsound import playsound
import cv2
import numpy as np
from PIL import Image
import speech_recognition as sr
import os
import time
import json
import cv2
import numpy as np
import HandTrackingModule as htm
import time
import autopy
from selenium_browser import Selenium_Browser
from utilities import start_micro, start_recognition, background_startup, start_sound, play, getGesturesHelp, thread_with_exception
from micro import microphone
class hand_gesture_browser():
    def __init__(self, cap, detector, user):
        self.container = [0, 0, 0, 0, 0]
        self.last_click_time = 0
        self.last_right_click_time = 0
        self.clicked = 0
        self.user = user
        self.in_search_bar = False
        self.old_text = 'https://www.youtube.com/'
        self.scroll_semaphore = 0
        self.main(cap, detector)

    def get_controlled_scroll(self, img, lmlist, wCam, hCam):
        if self.scroll_semaphore == 3:
            #print("In controlled sroll")
            cv2.line(img, (0, hCam // 2 - 60), (wCam, hCam // 2 - 60), (0, 255, 0), 2)
            cv2.line(img, (0, hCam // 2 + 60), (wCam, hCam // 2 + 60), (0, 255, 0), 2)
            if hCam // 2 - 60 <= lmlist[10][2] <= hCam // 2 + 60:
                return
            if lmlist[10][2] < hCam // 2 - 60:
                distance = ((hCam // 2 - 30) - lmlist[10][2])*0.04
            else:
                distance = ((hCam // 2 + 30) - lmlist[10][2])*0.04

            pyautogui.scroll(distance)
        else:
            self.scroll_semaphore+=1



    def get_right_click(self,img):

        length, img, lineInfo = detector.findDistance(12, 4, img)
        #print("right len", length)
        if length < 50 and time.time() - self.last_right_click_time > 1.5:
            autopy.mouse.click(autopy.mouse.Button.RIGHT)
            self.last_right_click_time = time.time()

    def get_click(self, fingers, img, b, coords, plocX, plocY, wScreen, a1, a2,b1,b2,c1,c2,d1,d2, obj):
        length, img, lineInfo = detector.findDistance(8, 4, img)


        if length < 50 and time.time() - self.last_click_time > 1.5:
            self.clicked+=1
            if self.clicked == 2:
                autopy.mouse.click()
                b.check_input_cell(obj)
                self.last_click_time = time.time()
                self.clicked = 0
                print("clicked")
                self.getSearchBarClick(plocX, plocY, a1, a2, b1, b2, c1, c2, d1, d2, b, obj)

        else:
            if self.clicked>0:
                self.clicked-=1
        #print("Click semaphore", self.clicked)

    def getSearchBarClick(self, plocX, plocY, ax, ay, bx, by, cx, cy, dx, dy, driver, obj):

        if plocX > ax and plocY > ay \
            and plocX > dx and plocY < dy \
            and plocX < bx and plocY > by \
            and plocX < cx and plocY < cy:
            print("In search bar click")
            text = driver.get_speech(obj)

            try:
                for i in range(len(self.old_text)): #Find best way
                    pyautogui.press('backspace')
                pyautogui.write(text)
                self.old_text = text

            except:
                print("error")
            self.last_click_time = time.time()




    def get_screenshot(self, img, b):
        length, img, lineInfo = detector.findDistance(4, 8, img)
        if length < 50 and time.time() - self.last_click_time > 1.5:
            self.last_click_time = time.time()
            b.get_browser_screenshot()
            start_sound("screenshot.mp3", 1)

    def get_mouse_movement(self, fingers, img, frameR, wCam, hCam, wScr, hScr, smoothening, plocX, plocY, x13, y13, x1,
                           y1):
        #print("In get mouse movement")
        # 5. Convert Coordinates
        x3 = np.interp(x13, (frameR, wCam - frameR), (0, wScr))
        y3 = np.interp(y13, (frameR, hCam - frameR), (0, hScr))
        # 6. Smoothen Values
        clocX = plocX + (x3 - plocX) / smoothening
        clocY = plocY + (y3 - plocY) / smoothening
        # 7. Move Mouse
        try:
            autopy.mouse.move(wScr - clocX, clocY)
        except:
            pass
        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        plocX, plocY = clocX, clocY
        return plocX, plocY

    def get_movement(self, lmList, fingers, acquired):
        #print("In get movement")
        if sum(fingers) >= 4:
            self.container.insert(0, lmList[8][1])
        else:
            self.container.insert(0, None)
        if len(self.container) > 10:
            self.container = self.container[:-1]
        # print("container", self.container)
        difference = 0
        if len(self.container) > 4:
            if None not in self.container:
                for i in range(len(self.container) - 1):
                    difference += self.container[i] - self.container[i + 1]
            else:
                difference = None
        if difference != None:
            # print("Difference =>", difference)
            if difference > 60:
                # print("\nRIGHT\n")
                return ("right2left")
            if difference < -60:
                # print("\nLeft\n")
                return ("left2right")
        else:
            return None

    def close(self, b):
        start_sound('close.mp3', 2.5)
        time.sleep(3)
        if self.user['username'] != "GuestUser":
            b.save_user_tabs(self.user)
        import psutil
        b.browser.quit()
        PROCNAME = "python3"
        for proc in psutil.process_iter():
            print(proc.name())
            # check whether the process name matches
            if proc.name() == PROCNAME:
                proc.kill()
        exit()

    def main(self, cap, detector):
        try:
            ##########################
            detector.counter = 0
            wCam, hCam = 640, 480
            frameR = 120  # Frame Reduction
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
            b.get_user_tabs(self.user)
            coords = None
            time.sleep(1)
            while coords is None:
                coords = pyautogui.locateOnScreen("find_me3.png")
                print(coords)
            print("Cordinate ", coords)
            a1, a2 = int(coords.left + coords.width), coords.top
            b1, b2 = int(wScr - coords.width), coords.top
            c1, c2 = int(wScr - coords.width), int(coords.top + coords.height)
            d1, d2 = int(coords.left + coords.width), int(coords.top + coords.height)
            gesture_help_thread = thread_with_exception('Thread 1')
            gesture_help_thread.start()

            while True:

                # 1. Find hand Landmarks
                success, img = cap.read()
                img = detector.findHands(img)
                lmList, current_hand, counter = detector.findPosition(img)
                if counter > 50:
                    self.close(b)

                # 2. Get the tip of the index and middle fingers
                if len(lmList) != 0:
                    x1, y1 = lmList[8][1:]
                    x13, y13 = lmList[13][1:]
                    x2, y2 = lmList[12][1:]
                    fingers = detector.fingersUp()

                    cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR),
                                  (255, 0, 255), 2)

                    movement = self.get_movement(lmList, fingers, acquired)

                    if time.time() - time_since_tab_switch > time_to_wait_after_tab_switch:
                        recovered = True
                    if movement != None and recovered:
                        b.switch_to_tab(movement)
                        time_since_tab_switch = time.time()
                        recovered = False


                    if fingers == [0, 0, 0, 0, 0]:
                        self.get_controlled_scroll(img, lmList, wCam, hCam)
                    elif fingers == [1, 1, 0, 0, 1]:
                        self.get_screenshot(img, b)
                    elif fingers[0] == 1 and fingers[1] == 1 and fingers[2]==0:
                        self.get_click(fingers, img, b, coords, plocX, plocY, wScr, a1, a2,b1,b2,c1,c2,d1,d2,  gesture_help_thread)

                    elif fingers == [1,1,1,0,0]:
                        self.get_right_click(img)
                    elif fingers == [0, 1, 0, 0, 0]:
                        plocX, plocY = self.get_mouse_movement(fingers, img, frameR, wCam, hCam, wScr, hScr,
                                                               smoothening, plocX, plocY, x13, y13 - 50, x1, y1)
                    if fingers != [0,0,0,0,0] and self.scroll_semaphore>=0:
                        self.scroll_semaphore-=1

                cTime = time.time()
                fps = 1 / (cTime - pTime)
                pTime = cTime
                img = cv2.flip(img, 1)
                cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                            (255, 0, 0), 3)

        except selenium.common.exceptions.NoSuchWindowException:
            b.switch_to_tab("right2left", closing = True)




import  threading

if __name__ == '__main__':

    print("OH")
    background = True #If true the program starts in background: raise 2 hands to start it
    use_face_recognition = True
    detector = htm.handDetector(maxHands=2, dominant='Right')
    done = False
    try:
        print("trying")
        cap = cv2.VideoCapture(-1)
    except:
        i=10
        while done == False:
            try:
                print("I", i)
                cap = cv2.VideoCapture(i)
                done = True
            except:
                i-=1



    pygame.init()
    pygame.mixer.init()
    if background:
        start_sound('start_speech.mp3', 1)
        background_startup(detector, cap)


    print("CAP", cap)
    cap.release()
    if use_face_recognition:
        user = start_recognition()
        print(user)
    cap = cv2.VideoCapture(-1)
    detector = htm.handDetector(maxHands=2, dominant=user['dominant'])
    
    start_sound('start.mp3', 10.5)
    v = hand_gesture_browser(cap, detector, user)

