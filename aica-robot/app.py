from flask import Flask,render_template,request,jsonify
import pyttsx3, os, random
import speech_recognition as sr

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
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Im Listening...")
        text_to_speech("Im Listening...")
        audio_clip = recognizer.listen(source, phrase_time_limit = 7)
        try:
            recognized_text = recognizer.recognize_google(audio_clip)
        except sr.UnknownValueError:
            recognized_text = "Sorry I can't here you."
        except sr.RequestError:
            recognized_text = "Failed to connect to Google API."
    
    return jsonify({'speech': recognized_text})

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

if __name__ == '__main__':
    app.run(port=5000,debug=True)