from colorama import Fore
from functions import *
import os
from flask import request

DIR =   "/home/ubuntu/RealVC/"

def RVC(request):
    data = request.get_json()
    file_path = data.get('input_file')
    voice_name = data.get('voice_name')
    
    file_path = check_file_exist(file_path)
    output_path = RVC_gen(file_path,voice_name)

    return f"13.200.241.87/get-file/{file_path.split("/")[-1]}"


def RVC_gen(input_path,model_name):
    if not model_name:
        model_name = "Amitabh-Voice"
    if not input_path:
        print("input_path Error")
    LAST_DIR = os.getcwd()
    os.chdir(f"{DIR}RVC")

    model_path = f"{DIR}RVC/assets/weights/{model_name}.pth"#@param {type:"string"}
    index_path = f"{DIR}RVC/logs/{model_name}/"#@param {type:"string"}
    index_path = Prefix_find(index_path,"added")

    print(Fore.GREEN + f"{index_path} was found") if os.path.exists(index_path) else print(Fore.RED + f"{index_path} was not found")
    pitch = 0 # @param {type:"slider", min:-12, max:12, step:1}

    # input_path = f"{DIR}RVC/audios/astronauts.mp3"#@param {type:"string"}

    if not os.path.exists(input_path):
        raise ValueError(f"{input_path} was not found in your RVC folder.")

    os.environ['index_root']  = os.path.dirname(index_path)
    index_path = os.path.basename(index_path)
    f0_method = "rmvpe" # @param ["rmvpe", "pm", "harvest"]
    # save_as = f"{DIR}RVC/audios/cli_output.wav"#@param {type:"string"}
    save_as = "/home/ubuntu/Server/Output_mp3/"+gen_name()+".mp3"
    model_name = os.path.basename(model_path)
    os.environ['weight_root'] = os.path.dirname(model_path)
    index_rate = 0.5 # @param {type:"slider", min:0, max:1, step:0.01}
    volume_normalization = 0 #param {type:"slider", min:0, max:1, step:0.01}
    consonant_protection = 0.5 #param {type:"slider", min:0, max:1, step:0.01}

    import subprocess
    command = f"rm -f {save_as}"
    result = subprocess.run(command, shell=True, check=True)

    command = f"python tools/cmd/infer_cli.py --f0up_key {pitch} --input_path {input_path} --index_path {index_path} --f0method {f0_method} --opt_path {save_as} --model_name {model_name} --index_rate {index_rate} --device 'cuda:0' --is_half True --filter_radius 3 --resample_sr 0 --rms_mix_rate {volume_normalization} --protect {consonant_protection}"
    result = subprocess.run(command,shell=True, check=True)

    print("Output File Generated: ",save_as)
    os.chdir(LAST_DIR)
    
    return save_as


def Prefix_find(root_path, prefix):
    for dirpath, _, filenames in os.walk(root_path):
        for filename in filenames:
            if filename.startswith(prefix):
                return os.path.join(dirpath, filename)
    return None

def check_file_exist(download_path):
    downloads = "/home/ubuntu/Server/Output_mp3/"
    file_name = download_path.split('/')[-1]

    if not os.path.exists(downloads+file_name):
        command = "wget -P /home/ubuntu/Server/Output_mp3/ {download_path}"
        result = subprocess.run(command, shell=True, check=True)
        print(f"downloaed file {file_name}")

    return downloads+file_name