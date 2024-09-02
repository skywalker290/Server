import torch
from TTS.api import TTS # type: ignore
from functions import *
from IndicTTS import indicTTS


device = "cuda" if torch.cuda.is_available() else "cpu"

tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

def cloner(text,lang,input_wav,output_path):
    tts.tts_to_file(text=text, speaker_wav=input_wav, language=lang, file_path=output_path)
    


def Cloner(request):
    PUBLIC_IP = "13.200.241.87"
    data = request.get_json()
    
    input_wav = data.get('input_wav')
    language = data.get('language')
    input_text = data.get('text')
    name = data.get('name')
    phone = data.get('phone')
    email = data.get('email')

    if not (name and phone and email):
        return "specify,Trace Parameters", 400

    if not language:
        return "specify, language", 400
    else:
        if(language!='en'):
            return indicTTS(request)
        
    pitch_change = data.get('pitch')
    speed_change = data.get('speed')
    decibel_change = data.get('decibel')

    output_file = gen_name() + '.wav'

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
    
    cloner(text=text, lang=output_language, input_wav=input_file, output_path=output_path)
    modify_audio(output_path,pitch_change=pitch_change,decibel_change=decibel_change,speed_change=speed_change)
    convert_wav_to_mp3(output_path,output_path[:-4]+'.mp3')
    os.remove(os.getcwd()+'/'+output_path)
    write_metadata(name,phone,email,output_path[:-4]+'.mp3')
    
    # return send_from_directory('.', 'output.mp3', as_attachment=True)
    return f"http://{PUBLIC_IP}/get-file/{output_file[:-4]+'.mp3'}"