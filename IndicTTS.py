from TTS.utils.synthesizer import Synthesizer
from functions import *
from Translate import  Translate_Eng_to_Indic
from dotenv import load_dotenv
import os
import time
load_dotenv()

PUBLIC_IP = os.getenv("PUBLIC_IP")


def init_synthesizer(language):
    model_path = f"models/v1/{language}/fastpitch/best_model.pth"
    config_path = f"models/v1/{language}/fastpitch/config.json"
    vocoder_path = f"models/v1/{language}/hifigan/best_model.pth"
    vocoder_config_path = f"models/v1/{language}/hifigan/config.json"
    gpu = False

    synthesizer = Synthesizer(
        tts_checkpoint=model_path,
        tts_config_path=config_path,
        tts_speakers_file=None,
        tts_languages_file=None,
        vocoder_checkpoint=vocoder_path,
        vocoder_config=vocoder_config_path,
        encoder_checkpoint=None,
        encoder_config=None,
        model_dir=None,
        use_cuda=gpu,
    )
    return synthesizer

def TTS_to_file(synthesizer,text,speaker_name,speaker_wav,pitch_change,speed_change,decibel_change,user):
    
    # relativeFilePath = f"/{user}/{int(time.time() * 1000)}.wav"
    # output_file = gen_name() + '.wav'
    output_file = f"{int(time.time() * 1000)}.wav"
    directory = f"AI4BharatMp3/{user}/"
    output_path =  directory + output_file

    if not os.path.exists(directory):
        # Create the directory
        os.makedirs(directory)
        # print(f"Directory '{directory}' created.")
    else:
        print(f"Directory '{directory}' already exists.")


    wav = synthesizer.tts(
        text=text,
        speaker_name=speaker_name,
        language_name=None,
        speaker_wav=speaker_wav,
        reference_wav=None,
        style_wav=None,
        style_text=None,
        reference_speaker_name=None,
        split_sentences=True,
    )

    synthesizer.save_wav(wav=wav, path=output_path)
    modify_audio(output_path,pitch_change=pitch_change,speed_change=speed_change,decibel_change=decibel_change)
    convert_wav_to_mp3(output_path,output_path[:-4]+'.mp3')
    os.remove(os.getcwd()+'/'+output_path)
    return output_file

def indicTTS(request):
    # PUBLIC_IP = "103.227.96.199"
    data = request.get_json()

    available_language = ['gu','hi','kn','ml','mni','mr','or','pa','raj','ta','te','as','bn','brx','en+hi','en']
    
    input_wav = data.get('input_wav')
    language = data.get('language')
    input_text = data.get('text')
    translate = data.get('translate') # To use Indic Translator Set it '1' or Else '0'
    speaker = data.get('gender')
    pitch_change = data.get('pitch')
    speed_change = data.get('speed')
    decibel_change = data.get('decibel')
    name = data.get('name')
    phone = data.get('phone')
    email = data.get('email')
    user =  email.replace("@gmail.com", "").replace(".","")
    
    # print(f"file name : {relativeFilePath}" )

    # Convert English Text to Indic Text
    if(translate and translate == '1'):
        input_text = Translate_Eng_to_Indic(input_text,language)[0]

    if(language not in available_language):
        return "Specify, Valid Language!" ,400

    speaker_name = "male"
    input_file = None
    text = ""
    if input_wav:
        input_file = 'Input_wavs/' + input_wav
    if speaker:
        speaker_name = speaker
    if input_text:
        text = input_text
    else:
        return "Pass the Text!", 400
    
    synthesizer = init_synthesizer(language=language)

    output_file = TTS_to_file(
            synthesizer=synthesizer,
            text=text,
            speaker_name=speaker_name,
            speaker_wav=input_file,
            speed_change=speed_change,
            decibel_change=decibel_change,
            pitch_change=pitch_change,
            user=user
        )

    write_metadata(name,phone,email,"AI4BharatMp3/"+output_file[:-4]+'.mp3')
    
    return f"https://{PUBLIC_IP}/get-file/{user}/{output_file[:-4]+'.mp3'}"
