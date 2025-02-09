from flask import Flask,render_template,request,jsonify,Response
import pyttsx3, os, random
import speech_recognition as sr
from camera import Video

app=Flask(__name__)

@app.route('/',methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/refresh_page',methods=['GET'])
def refresh_page():
    return render_template('index.html')

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
            servoPos = Video().get_servos()
            Video().send_coordinates_to_arduino(servoPos[0], servoPos[1])
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

def text_to_speech(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('rate', 125)
    engine.setProperty('voice', voices[0].id)
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
    app.run(port=5000,debug=True)
