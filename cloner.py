import torch
from TTS.api import TTS # type: ignore
from pydub import AudioSegment
from datetime import datetime


device = "cuda" if torch.cuda.is_available() else "cpu"

tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

def cloner(text,lang,input_wav,output_file):
    tts.tts_to_file(text=text, speaker_wav=input_wav, language=lang, file_path=output_file)
    convert_wav_to_mp3(output_file,output_file[:-4]+'.mp3')


def convert_wav_to_mp3(input_wav_file, output_mp3_file):
    audio = AudioSegment.from_wav(input_wav_file)    
    audio.export(output_mp3_file, format="mp3")
    print(f"Converted {input_wav_file} to {output_mp3_file}")


def gen_name():
    return str(datetime.now().strftime("%Y%m%d%H%M%S"))


def Cloner(request):
    PUBLIC_IP = "13.235.143.16"
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


    output_file = gen_name() + '.mp3'

    output_path = "Output_mp3/" + output_file
    
    input_file = "Input_wavs/obama.wav"

    output_language = "en"

    text = ""
    
    if input_wav:
        input_file = 'Input_wavs/' + input_wav
    if language:
        output_language = language
    if input_text:
        text = input_text
    else:
        return "Pass the Text!", 400
    
    cloner(text=text, lang=output_language, input_wav=input_file, output_file=output_path)
    
    # return send_from_directory('.', 'output.mp3', as_attachment=True)
    return f"http://{PUBLIC_IP}/get-file/{output_file}"