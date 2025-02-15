from flask import Flask,render_template,request,jsonify,Response
from camera import Video
from subprocess import call
import speech_recognition as sr
import sounddevice
import time
import pyttsx3
import requests
import json

app=Flask(__name__)

@app.route('/',methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/refresh_page',methods=['GET'])
def refresh_page():
    return render_template('index.html')

@app.route('/is_human_detected',methods=['POST'])
def get_track():
    if request.method == 'POST':
        is_human_detected = Video().is_human_detected()
        return jsonify({'is_human_detected': is_human_detected}) 

@app.route('/speech_start',methods=['POST'])
def speech_start():
    if request.method == 'POST':
        text = request.form.get("inputText")
        text_to_speech(text)
        return jsonify({'render_url': '/refresh_page'})
    
@app.route('/listen_start',methods=['POST'])
def listen_start():
    recognized_text = "Got Cha"
    role = "AICA"
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        if Video().is_human_detected() == True:
            text_to_speech("Hello how can I help you?")
            audio_clip = recognizer.listen(source, phrase_time_limit = 6) 
            try:
                recognized_text = recognizer.recognize_google(audio_clip)
                role = "User"
            except sr.UnknownValueError:
                recognized_text = "Sorry I can't here you."
                role = "AICA"
            except sr.RequestError:
                recognized_text = "Failed to connect to Google API."
                role = "AICA"
        else:
            recognized_text = ""
            role = ""
            
    return jsonify({'speech': recognized_text,'role': role})

@app.route('/send_track',methods=['POST'])
def send_track():
    if request.method == 'POST':
        servoPos = Video().get_servos()
        send_coordinates_to_arduino(servoPos[0], servoPos[1])

        return jsonify({'render_url': servoPos})

@app.route('/SendAIRequest',methods=['POST'])
def SendAIRequest():
    contMessage = request.form.get("contMessage")
    messages =[{
        "role": "user",
        "content": contMessage
    }]
    payload = {'messages': messages}
    url = "http://localhost:3000/api/conversation"
    headers = {'Content-Type': 'application/json', 'Accept':'application/json'}
    response = requests.post(
        url, 
        data=json.dumps(payload) , 
        headers=headers).json()
    print(response)
    return response    


@app.route('/get_track',methods=['POST'])
def get_track():
    if request.method == 'POST':
        servoPos = Video().get_servos()

        return jsonify({'render_url': servoPos})

def send_coordinates_to_arduino(x, y):
        try:
            coordinates = f"{x},{y}\r"
            ser = serial.Serial("COM5", 9600, timeout = 1)
            ser.write(coordinates.encode())
            print(coordinates.encode())
        except serial.SerialException as e:
            print("ERROR")
        except TypeError as e:
            print("ERROR")

def text_to_speech(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 110)
    engine.say(text)
    engine.runAndWait()
    engine.stop()
    if engine._inLoop:
        engine.endLoop()
    engine = None
    
def gen(camera):
    while True:
        frame=camera.get_frame()
        camera.is_human_detected()
        yield(b'--frame\r\n'
       b'Content-Type:  image/jpeg\r\n\r\n' + frame +
         b'\r\n\r\n')
    
@app.route('/video')
def video():
    return Response(gen(Video()),
    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
