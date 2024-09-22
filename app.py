from flask import Flask, request, jsonify, send_file, render_template
from cloner import *
from functions import *
from RVC import *
from flask_cors import CORS, cross_origin
from flask_socketio import SocketIO, emit
import os

app = Flask(__name__, static_url_path='/Output_mp3')
CORS(app)

# Initialize SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")

app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100 MB

# Event for WebSocket connection
@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('response', {'message': 'You are connected!'})

# Event for WebSocket disconnection
@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

# WebSocket event to send a greeting message (original "/" route)
@socketio.on('hello')
def hello_via_socket(data):
    emit('response', {'message': 'Helloo There!'})

# WebSocket event for GenerateVoice (original "/GenerateVoice/" route)
@socketio.on('GenerateVoice')
def clone_via_socket(data):
    check = check_credentials(data)
    if check != True:
        emit('response', {'error': check})
    else:
        result = Cloner(request=data)
        emit('response', {'result': result})

# WebSocket event to get file (original "/get-file/<filename>" route)
@socketio.on('get_file')
def get_file_via_socket(data):
    filename = 'Output_mp3/' + data.get('filename', '')
    try:
        emit('file', {'file_url': filename})
    except Exception as e:
        emit('response', {'error': str(e)})

# WebSocket event to list speakers (original "/list-speakers/" route)
@socketio.on('list_speakers')
def list_speakers_via_socket(data):
    check = check_credentials(data)
    if check != True:
        emit('response', {'error': check})
    else:
        speakers_list = list_files()
        emit('response', {'speakers': speakers_list})

# WebSocket event to refresh speakers (original "/refresh-speakers/" route)
@socketio.on('refresh_speakers')
def refresh_speakers_via_socket(data):
    check = check_credentials(data)
    if check != True:
        emit('response', {'error': check})
    else:
        git_pull("Input_wavs")
        speakers_list = list_files()
        emit('response', {'speakers': speakers_list})

# WebSocket event for Cloner (original "/Cloner/" route)
@socketio.on('Cloner')
def rvc_via_socket(data):
    check = check_credentials(data)
    if check != True:
        emit('response', {'error': check})
    else:
        result = RVC(request=data)
        emit('response', {'result': result})

# WebSocket event to list languages (original "/languages/" route)
@socketio.on('languages')
def show_languages_via_socket():
    text = {
        "gu": {"et": "Gujarati", "lt": "ગુજરાતી"},
        "hi": {"et": "Hindi", "lt": "हिंदी"},
        "kn": {"et": "Kannada", "lt": "ಕನ್ನಡ"},
        "ml": {"et": "Malayalam", "lt": "മലയാളം"},
        "mni": {"et": "Manipuri", "lt": "মণিপুরী"},
        "mr": {"et": "Marathi", "lt": "मराठी"},
        "or": {"et": "Oriya", "lt": "ଓଡ଼ିଆ"},
        "pa": {"et": "Punjabi", "lt": "ਪੰਜਾਬੀ"},
        "raj": {"et": "Rajasthani", "lt": "राजस्थानी"},
        "ta": {"et": "Tamil", "lt": "தமிழ்"},
        "te": {"et": "Telugu", "lt": "తెలుగు"},
        "as": {"et": "Assamese", "lt": "অসমীয়া"},
        "bn": {"et": "Bengali", "lt": "বাংলা"},
        "brx": {"et": "Bodo", "lt": "बर'"}
    }
    emit('response', {'languages': text})

# WebSocket event for file upload (original "/uploader" route)
@socketio.on('upload_file')
def upload_file_via_socket(data):
    try:
        f = data['file']
        filename = f.filename
        file_path = os.path.join("Output_mp3", filename)
        f.save(file_path)
        emit('response', {'message': 'File uploaded successfully', 'file_url': file_path})
    except Exception as e:
        emit('response', {'error': str(e)})

if __name__ == "__main__":
    # Use SocketIO to run the app with WebSocket support
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
