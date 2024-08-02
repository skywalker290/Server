from flask import Flask, request, send_from_directory
import os
from cloner import *
from flask import Flask, send_file
from functions import *
from flask_cors import CORS, cross_origin

app = Flask(__name__, static_url_path='/Output_mp3')
CORS(app)


@app.route("/GenerateVoice/", methods=['POST'])
def clone():
    check = check_credentials(request)
    if(check != True):
        return check
    return gen_json(Cloner(request=request))

@app.route('/get-file/<filename>', methods=['GET'])
def get_file(filename):
    filename='Output_mp3/'+filename 
    return send_file(filename, as_attachment=True)

@app.route('/list-speakers/',methods=['GET'])
def list_speakers():
    check = check_credentials(request)
    if(check != True):
        return check
    return list_files()

@app.route('/refresh-speakers/',methods=['GET'])
def refresh_speakers():
    check = check_credentials(request)
    if(check != True):
        return check
    git_pull("Input_wavs")
    return list_files()
@app.route('/languages/',methods=['GET'])
def show_languages():
    text = {
        "gu": {
            "et": "Gujarati",
            "lt": "ગુજરાતી"
        },
        "hi": {
            "et": "Hindi",
            "lt": "हिंदी"
        },
        "kn": {
            "et": "Kannada",
            "lt": "ಕನ್ನಡ"
        },
        "ml": {
            "et": "Malayalam",
            "lt": "മലയാളം"
        },
        "mni": {
            "et": "Manipuri",
            "lt": "মণিপুরী"
        },
        "mr": {
            "et": "Marathi",
            "lt": "मराठी"
        },
        "or": {
            "et": "Oriya",
            "lt": "ଓଡ଼ିଆ"
        },
        "pa": {
            "et": "Punjabi",
            "lt": "ਪੰਜਾਬੀ"
        },
        "raj": {
            "et": "Rajasthani",
            "lt": "राजस्थानी"
        },
        "ta": {
            "et": "Tamil",
            "lt": "தமிழ்"
        },
        "te": {
            "et": "Telugu",
            "lt": "తెలుగు"
        },
        "as": {
            "et": "Assamese",
            "lt": "অসমীয়া"
        },
        "bn": {
            "et": "Bengali",
            "lt": "বাংলা"
        },
        "brx": {
            "et": "Bodo",
            "lt": "बर'"
        }
    }

    return jsonify(text), 200




if __name__ == "__main__":
    app.run()

