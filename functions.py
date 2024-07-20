from flask import jsonify
import os
import subprocess
from pydub import AudioSegment
from datetime import datetime

def list_files():
    try:
        speaker_path = "Input_wavs"
        
        abs_folder_path = os.path.abspath(speaker_path)

        # List all files in the specified folder
        files = [f for f in os.listdir(abs_folder_path) if os.path.isfile(os.path.join(abs_folder_path, f))]
        
        return jsonify(files=files), 200

    except Exception as e:
        return jsonify(error=str(e)), 500
    


def git_pull(repo_path):
    try:
        result = subprocess.run(['git', '-C', repo_path, 'pull'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = result.stdout.decode('utf-8')
        return output
    except subprocess.CalledProcessError as e:
        return f"An error occurred: {e.stderr.decode('utf-8')}"
    
def check_credentials(request):
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
    
    return True



def convert_wav_to_mp3(input_wav_file, output_mp3_file):
    audio = AudioSegment.from_wav(input_wav_file)    
    audio.export(output_mp3_file, format="mp3")
    print(f"Converted {input_wav_file} to {output_mp3_file}")


def gen_name():
    return str(datetime.now().strftime("%Y%m%d%H%M%S"))

    