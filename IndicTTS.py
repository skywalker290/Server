from TTS.utils.synthesizer import Synthesizer
from functions import *

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

def TTS_to_file(synthesizer,text,speaker_name,speaker_wav):
    
    output_file = gen_name() + '.mp3'
    output_path = "Output_mp3/" + output_file

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
    convert_wav_to_mp3(output_path,output_path)
    return output_file

def indicTTS(request):
    PUBLIC_IP = "13.235.143.16"
    data = request.get_json()
    
    input_wav = data.get('input_wav')
    language = data.get('language')
    input_text = data.get('text')
    speaker = data.get('speaker_name')

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
        speaker_wav=input_file
        )
    
    return f"http://{PUBLIC_IP}/get-file/{output_file}"