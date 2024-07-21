from flask import jsonify
import os
import subprocess
from pydub import AudioSegment
from datetime import datetime
from pydub import AudioSegment

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




def change_pitch(audio_segment, semitones):
    new_sample_rate = int(audio_segment.frame_rate * (2.0 ** (semitones / 12.0)))
    return audio_segment._spawn(audio_segment.raw_data, overrides={'frame_rate': new_sample_rate}).set_frame_rate(audio_segment.frame_rate)

def change_speed(audio_segment, speed=1.0):
    return audio_segment._spawn(audio_segment.raw_data, overrides={
         "frame_rate": int(audio_segment.frame_rate * speed)
    }).set_frame_rate(audio_segment.frame_rate)

def change_volume(audio_segment, decibels):
    return audio_segment + decibels

def modify_audio(input_file, pitch_change, speed_change, decibel_change):
    # Load audio file using pydub
    audio = AudioSegment.from_file(input_file)

    # Change pitch
    if pitch_change:
        pitch_change = float(pitch_change)
        audio = change_pitch(audio, pitch_change)
    
    # Change speed
    if speed_change:
        speed_change = float(speed_change)
        audio = change_speed(audio, speed_change)
    
    # Change volume
    if decibel_change:
        decibel_change = float(decibel_change)
        audio = change_volume(audio, decibel_change)
    
    # Export the modified audio
    audio.export(input_file, format="wav")
    print(f'Modified audio saved as {input_file}')



# Example usage
# modify_audio('/home/skywalker/#/Server/Input_wavs/hindi_output.wav', '/home/skywalker/#/Server/Output_mp3/modified_ouput.wav', pitch_change=-2, speed_change=1, decibel_change=5)


    