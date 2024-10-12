
# # https://colab.research.google.com/github/AI4Bharat/IndicTrans2/blob/main/huggingface_interface/colab_inference.ipynb#scrollTo=6OG3Bw-sHnf3
# # Indictrans2

import torch
from transformers import AutoModelForSeq2SeqLM, BitsAndBytesConfig, AutoTokenizer
from IndicTrans2.huggingface_interface.IndicTransToolkit.IndicTransToolkit import IndicProcessor

BATCH_SIZE = 4
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
quantization = None

def initialize_model_and_tokenizer(ckpt_dir, quantization):
    if quantization == "4-bit":
        qconfig = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_compute_dtype=torch.bfloat16,
        )
    elif quantization == "8-bit":
        qconfig = BitsAndBytesConfig(
            load_in_8bit=True,
            bnb_8bit_use_double_quant=True,
            bnb_8bit_compute_dtype=torch.bfloat16,
        )
    else:
        qconfig = None

    tokenizer = AutoTokenizer.from_pretrained(ckpt_dir, trust_remote_code=True)
    model = AutoModelForSeq2SeqLM.from_pretrained(
        ckpt_dir,
        trust_remote_code=True,
        low_cpu_mem_usage=True,
        quantization_config=qconfig,
    )

    if qconfig == None:
        model = model.to(DEVICE)
        if DEVICE == "cuda":
            model.half()

    model.eval()

    return tokenizer, model


def batch_translate(input_sentences, src_lang, tgt_lang, model, tokenizer, ip):
    translations = []
    for i in range(0, len(input_sentences), BATCH_SIZE):
        batch = input_sentences[i : i + BATCH_SIZE]

        # Preprocess the batch and extract entity mappings
        batch = ip.preprocess_batch(batch, src_lang=src_lang, tgt_lang=tgt_lang)

        # Tokenize the batch and generate input encodings
        inputs = tokenizer(
            batch,
            truncation=True,
            padding="longest",
            return_tensors="pt",
            return_attention_mask=True,
        ).to(DEVICE)

        # Generate translations using the model
        with torch.no_grad():
            generated_tokens = model.generate(
                **inputs,
                use_cache=True,
                min_length=0,
                max_length=256,
                num_beams=5,
                num_return_sequences=1,
            )

        # Decode the generated tokens into text

        with tokenizer.as_target_tokenizer():
            generated_tokens = tokenizer.batch_decode(
                generated_tokens.detach().cpu().tolist(),
                skip_special_tokens=True,
                clean_up_tokenization_spaces=True,
            )

        # Postprocess the translations, including entity replacement
        translations += ip.postprocess_batch(generated_tokens, lang=tgt_lang)

        del inputs
        torch.cuda.empty_cache()

    return translations

def Translate_Eng_to_Indic(eng_text,target_lang):
    en_indic_ckpt_dir = "ai4bharat/indictrans2-en-indic-1B"  # ai4bharat/indictrans2-en-indic-dist-200M
    en_indic_tokenizer, en_indic_model = initialize_model_and_tokenizer(en_indic_ckpt_dir, quantization)
    ip = IndicProcessor(inference=True)
    src_lang = "eng_Latn"

    language_mapping = {
        "gu": "guj_Gujr",
        "hi": "hin_Deva",
        "kn": "kan_Knda",
        "ml": "mal_Mlym",
        "mni":"mni_Mtei",  # Manipuri has two variants
        "mr": "mar_Deva",
        "or": "ory_Orya",
        "pa": "pan_Guru",
        "raj":"hin_Deva",  # Rajasthani is not included in AI4Bharat's model
        "ta": "tam_Taml",
        "te": "tel_Telu",
        "as": "asm_Beng",
        "bn": "ben_Beng",
        "brx": "brx_Deva"
    }

    eng_text = [eng_text]

    tgt_lang = language_mapping[target_lang]

    Translated_text = batch_translate(eng_text, src_lang, tgt_lang, en_indic_model, en_indic_tokenizer, ip)

    return Translated_text
