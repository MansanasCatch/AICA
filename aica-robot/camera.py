import cv2
import numpy as np
import serial
import time

isHumanDetected = False

class Video(object):
    def send_coordinates_to_arduino(self,x, y, w, h):
        try:
            self.board.isOpen()
            coordinates = f"{x},{y}\r"
            self.board.write(coordinates.encode())
            print(coordinates)
        except IOError: 
            self.board.close()
            self.board.open()
    def __init__(self):
        print("INIT")
        with serial.Serial() as ser:
                ser.baudrate = 9600
                ser.port = 'COM4'
                self.board = ser
        
        self.video=cv2.VideoCapture(0)
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    def __del__(self):
        self.video.release()
    def is_human_detected(self):
        return isHumanDetected
    def get_frame(self):
        success, img = self.video.read()
        global isHumanDetected 
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.05, 8, minSize=(120,120))
        
        if len(faces) > 0:
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 5)
                #self.send_coordinates_to_arduino(x, y, w, h)
            
            isHumanDetected = True
            cv2.putText(img, "Face Detected", (50, 50), cv2.FONT_HERSHEY_PLAIN, 3, (20, 255, 1), 3 )
        else:
            isHumanDetected = False
            cv2.putText(img, "Detecting...", (50, 50), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)

        # cv2.putText(img, f'Servo X: {int(servoPos[0])} deg', (50, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
        # cv2.putText(img, f'Servo Y: {int(servoPos[1])} deg', (50, 100), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
        
        success,jpg=cv2.imencode('.jpg',img)
        return jpg.tobytes()
