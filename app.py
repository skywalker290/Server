from flask import Flask, request, send_from_directory, render_template
import os
from cloner import *
from flask import Flask, send_file
from functions import *
from flask_cors import CORS, cross_origin
from RVC import *
from Translate import Traslate_Request
from trasliteration import *

app = Flask(__name__, static_url_path='/AI4BharatMp3')
CORS(app)

app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100 MB

@app.route("/")
def hello():
    return gen_json("Helloo There!")

@app.route("/generate-voice", methods=['POST'])
def clone():
    check = check_credentials(request)
    if(check != True):
        return check
    return gen_json(Cloner(request=request))

@app.route('/get-file/<user>/<filename>', methods=['GET'])
def get_file(user,filename):
    filename= f"AI4BharatMp3/{user}/{filename}"  
    return send_file(filename, as_attachment=True)

@app.route('/list-speakers',methods=['GET'])
def list_speakers():
    check = check_credentials(request)
    if(check != True):
        return check
    return list_files()

@app.route('/refresh-speakers',methods=['GET'])
def refresh_speakers():
    check = check_credentials(request)
    if(check != True):
        return check
    git_pull("Input_wavs")
    return list_files()

@app.route('/cloner',methods=['POST'])
def rvc():
    check = check_credentials(request)
    if(check != True):
        return check
    return gen_json(RVC(request))

@app.route('/languages', methods=['GET'])
def show_languages():
    text = {
        "gu": {"et": "Gujarati", "lt": "ગુજરાતી"},
        "hi": {"et": "Hindi", "lt": "हिंदी"},
        "kn": {"et": "Kannada", "lt": "ಕನ್ನಡ"},
        "ml": {"et": "Malayalam", "lt": "മലയാളം"},
        "mni": {"et": "Manipuri", "lt": "মণিপুরী"},
        "mr": {"et": "Marathi", "lt": "मराठी"},
        "or": {"et": "Oriya", "lt": "ଓଡ଼ିଆ"},
        "pa": {"et": "Punjabi", "lt": "ਪੰਜਾਬੀ"},
        "raj": {"et": "Rajasthani(Traslation Not Available)", "lt": "राजस्थानी"},
        "ta": {"et": "Tamil", "lt": "தமிழ்"},
        "te": {"et": "Telugu", "lt": "తెలుగు"},
        "as": {"et": "Assamese", "lt": "অসমীয়া"},
        "bn": {"et": "Bengali", "lt": "বাংলা"},
        "brx": {"et": "Bodo", "lt": "बर'"}
    }

    # Directory containing model folders
    directory = "models/v1/"
    
    # Get the list of folder names in the 'models/v1/' directory
    models = [name for name in os.listdir(directory) if os.path.isdir(os.path.join(directory, name))]
    
    # Filter the 'text' dictionary to return only data for models present in 'models'
    filtered_text = {key: value for key, value in text.items() if key in models}
    
    return jsonify(filtered_text), 200
@app.route('/upload')
def upload_filee():
   return render_template('upload.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      file_path = os.path.join("AI4BharatMp3", f.filename)
      f.save(file_path)
      return 'file uploaded successfully'

@app.route('/vai')
def serve_vai():
    return render_template('VAI.html')

@app.route('/indictrans',methods = ['POST'])
def Eng_to_Indic():
    check = check_credentials(request)
    if(check != True):
        return check
    return gen_json(Traslate_Request(request=request))

@app.route('/transword',methods = ['POST'])
def Transliterate_word():
    check = check_credentials(request)
    if(check != True):
        return check
    return gen_json(Translit_word(request))

@app.route('/transtext',methods = ['POST'])
def Transliterate_text():
    check = check_credentials(request)
    if(check != True):
        return check
    return gen_json(Transliterate_text(request))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, ssl_context="adhoc", debug=True)