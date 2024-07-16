from flask import Flask, request, send_from_directory
import os
from cloner import *
from flask import Flask, send_file

app = Flask(__name__, static_url_path='/')

@app.route("/", methods=['POST'])
def hello():
    PUBLIC_IP = "127.0.0.1"
    MY_KEY = "7865"
    data = request.get_json()
    
    if not data:
        return "Invalid request: No JSON payload found", 400
    
    KEY = data.get('KEY')
    
    if(KEY):
        if(KEY != MY_KEY):
            return "Authorization Failed [Incorrect Credentials]!", 401
    else:
        return "Authorization Failed [Key Not Found]!", 401
    
    input_wav = data.get('input_wav')
    language = data.get('language')
    input_text = data.get('text')
    output_file = "output.mp3"
    input_file = "obama.wav"
    model_name = "tts_models/multilingual/multi-dataset/xtts_v2"
    output_language = "en"
    text = ""
    
    if input_wav:
        input_file = input_wav
    if language:
        output_language = language
    if input_text:
        text = input_text
    else:
        return "Pass the Text!", 400
    
    cloner(text=text, lang=output_language, input_wav=input_file, output_file=output_file)
    
    # return send_from_directory('.', 'output.mp3', as_attachment=True)
    return f"http://{PUBLIC_IP}/get-file/{output_file}"


@app.route('/get-file/<filename>', methods=['GET'])
def get_file(filename):
    return send_file(filename, as_attachment=True)

if __name__ == "__main__":
    app.run()

