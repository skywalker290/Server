from flask import jsonify
import os
import subprocess

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