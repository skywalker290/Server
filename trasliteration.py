from ai4bharat.transliteration import XlitEngine
# out = e._transliterate_sentence("hello", src_lang = "en", tgt_lang= 'hi')

def Translit_word(request):
    data = request.get_json()
    # src_lang = data.get("src")
    tgt_lang = data.get("tgt")
    text = data.get("text")
    count = data.get("count")

    # if not (src_lang):
    #     src_lang = "en"
    if not (tgt_lang):
        return "Specify, tgt_lang!", 500
    if not (text):
        return "No Text found!", 500
    if not (count):
        count = 3

    translit_engine = XlitEngine(tgt_lang, beam_width=4, rescore=True, src_script_type="en")

    output_text = translit_engine._transliterate_word(text, src_lang="en", tgt_lang=tgt_lang, topk=int(count))

    return output_text, 200

def Translit_text(request):
    data = request.get_json()
    # src_lang = data.get("src")
    tgt_lang = data.get("tgt")
    text = data.get("text")

    if not (tgt_lang):
        return "Specify, tgt_lang!", 500
    if not (text):
        return "No Text found!", 500

    translit_engine = XlitEngine(tgt_lang, beam_width=4, rescore=True, src_script_type="en")

    output_text = translit_engine._transliterate_sentence(text, src_lang = "en", tgt_lang=tgt_lang)

    return output_text, 200
    




    


    
