import cv2
from cvzone.FaceDetectionModule import FaceDetector
import numpy as np

isHumanDetected = False
ws, hs = 1280, 720
detector = FaceDetector()
servoPos = [90, 90]

class Video(object):
    def __init__(self):
        self.video=cv2.VideoCapture(0)
        self.video.set(3, ws)
        self.video.set(4, hs)
    def __del__(self):
        self.video.release()
    def is_human_detected(self):
        return isHumanDetected
    def get_servos(self):
        return servoPos
    def get_frame(self):
        global isHumanDetected
        success, img = self.video.read()
        img = cv2.flip(img, 1)
        img, bboxs = detector.findFaces(img, draw=False)

        if bboxs:
            fx, fy = bboxs[0]["center"][0], bboxs[0]["center"][1]
            pos = [fx, fy]
            servoX = np.interp(fx, [0, ws], [0, 180])
            servoY = np.interp(fy, [0, hs], [0, 180])

            if servoX < 0:
                servoX = 0
            elif servoX > 180:
                servoX = 180
            if servoY < 0:
                servoY = 0
            elif servoY > 180:
                servoY = 180

            servoPos[0] = servoX
            servoPos[1] = servoY

            isHumanDetected = True
            cv2.putText(img, "Face Detected", (50, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3 )
            cv2.line(img, (0, fy), (ws, fy), (0, 0, 0), 2)  # x line
            cv2.line(img, (fx, hs), (fx, 0), (0, 0, 0), 2)  # y line
        else:
            isHumanDetected = False
            cv2.putText(img, "Scanning...", (50, 50), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)
            cv2.line(img, (0, 360), (ws, 360), (0, 0, 0), 2)  # x line
            cv2.line(img, (640, hs), (640, 0), (0, 0, 0), 2)  # y line

        success,jpg=cv2.imencode('.jpg',img)
        return jpg.tobytes()
