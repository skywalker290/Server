import torch
from TTS.api import TTS
from pydub import AudioSegment


device = "cuda" if torch.cuda.is_available() else "cpu"

tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

def cloner(text,lang,input_wav,output_file):
    tts.tts_to_file(text=text, speaker_wav=input_wav, language=lang, file_path=output_file)
    convert_wav_to_mp3(output_file,output_file[:-4]+'.mp3')

def convert_wav_to_mp3(input_wav_file, output_mp3_file):
    audio = AudioSegment.from_wav(input_wav_file)    
    audio.export(output_mp3_file, format="mp3")
    print(f"Converted {input_wav_file} to {output_mp3_file}")