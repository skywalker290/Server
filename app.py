from flask import Flask, request, send_from_directory
import os
from cloner import *
from flask import Flask, send_file
from functions import *

app = Flask(__name__, static_url_path='/Output_mp3')

@app.route("/", methods=['POST'])
def clone():
    check = check_credentials(request)
    if(check != True):
        return check
    return Cloner(request=request)

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
    text = """
    Available:
    'hi' : "Hindi - हिंदी",
    'kn' : "Kannada - ಕನ್ನಡ",
    'ml' : "Malayalam - മലയാളം",
    'mr' : "Marathi - मराठी",
    'or' : "Oriya - ଓଡ଼ିଆ",
    'ta' : "Tamil - தமிழ்",
    'te' : "Telugu - తెలుగు",
    
    Upcomming:
    'as' : "Assamese - অসমীয়া",
    'bn' : "Bangla - বাংলা",
    'brx': "Boro - बड़ो",
    'gu' : "Gujarati - ગુજરાતી",
    'pa' : "Punjabi - ਪੰਜਾਬੀ",
    'raj': "Rajasthani - राजस्थानी",
    'mni': "Manipuri - মিতৈলোন",
    """
    return text, 200




if __name__ == "__main__":
    app.run()

