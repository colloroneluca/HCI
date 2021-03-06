import cv2
import mediapipe as mp
import time
import math
import numpy as np


class handDetector():
    def __init__(self, mode=False, maxHands=2, dominant='Right',detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.dominant = dominant
        self.ind = 0
        self.counter = 0
        self.current_hand = ''
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]

    def findHands(self, img, draw=True):
        try:
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        except:
            return None
        self.results = self.hands.process(imgRGB)
        # print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,
                                               self.mpHands.HAND_CONNECTIONS)

        return img
    def get_current_hands(self):
        myhands = []
        for hand in self.results.multi_handedness:
            myhands.append(hand.classification[0].label)
        return myhands

    def findPosition(self, img, handNo=0, draw=True):
        xList = []
        yList = []
        bbox = []
        myhands = []
        current_hand = None
        self.lmList = []
        if self.results.multi_hand_landmarks:
            try:
                myhands = self.get_current_hands()
                self.ind = (myhands.index(self.dominant)-1)%2

                myHand = self.results.multi_hand_landmarks[self.ind]
                current_hand = myhands[self.ind]
            except:
                myHand = self.results.multi_hand_landmarks[0]
                current_hand = myhands[0]
            for id, lm in enumerate(myHand.landmark):
                # print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                xList.append(cx)
                yList.append(cy)
                # print(id, cx, cy)
                self.lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

            xmin, xmax = min(xList), max(xList)
            ymin, ymax = min(yList), max(yList)
            bbox = xmin, ymin, xmax, ymax

            if draw:
                cv2.rectangle(img, (xmin - 20, ymin - 20), (xmax + 20, ymax + 20),
                              (0, 100, 0), 2)
            if current_hand == 'Left':
                current_hand = 'Right'
            elif current_hand == "Right":
                current_hand = "Left"
            self.current_hand = current_hand

        if len(myhands) == 2:
            if self.fingersUp() == [1,1,1,1,1]:
                self.counter +=1
            elif self.counter > 0:
                self.counter -= 1
        elif self.counter > 0:
            self.counter -=1

        return self.lmList, current_hand, self.counter

    def fingersUp(self):

        if len(self.lmList) > 0:
            fingers = []
            # Thumb
            if self.current_hand == 'Right':
                if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0] - 1][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            if self.current_hand == 'Left':
                if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0] - 1][1]:
                    fingers.append(0)
                else:
                    fingers.append(1)

            # Fingers
            for id in range(1, 5):

                if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            # totalFingers = fingers.count(1)

            return fingers
        else:
            return None

    def findDistance(self, p1, p2, img, draw=True,r=15, t=3):
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), t)
            cv2.circle(img, (x1, y1), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (cx, cy), r, (0, 0, 255), cv2.FILLED)
        length = math.hypot(x2 - x1, y2 - y1)

        return length, img, [x1, y1, x2, y2, cx, cy]
    #################################################################??

    ##################################################################

def main():

    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(-1)
    print("acquired video ")
    detector = handDetector(maxHands=2, dominant='Right')
    print("created detector")
    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        img = detector.findHands(img)
        lmList = detector.findPosition(img)
        fingers = detector.fingersUp(None)
        print(fingers, "\n")
        if len(lmList) != 0:
            # print(lmList)
            pass
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 255), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":

    main()
