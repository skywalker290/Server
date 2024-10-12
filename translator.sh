git clone https://github.com/AI4Bharat/IndicTrans2.git
cd IndicTrans2/huggingface_interface
python -m pip install nltk sacremoses pandas regex mock transformers>=4.33.2 mosestokenizer
python -c "import nltk; nltk.download('punkt')"
python -m pip install bitsandbytes scipy accelerate datasets
python -m pip install sentencepiece
git clone https://github.com/VarunGumma/IndicTransToolkit.git
cd IndicTransToolkit
python -m pip install --editable ./
cd ..