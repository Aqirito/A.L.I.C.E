
# LangPlusWaifu
*Tested in Windows with Pytorch 2.0.0 with CUDA 11.7*
*Python 3.10*
*pip 23.2.1*
*langchain 0.0.245*

### My specs:
* Nvidia RTX 3060 12 GB
* Intel i5 12400

*This work only for Llama type GPTQ model for now.*

*I will add type GGML model soon.*

*the default voice is from character named Kamisato Yayaka from video game called Genshin Impact.*

Model tested:
* [TheBloke/Pygmalion-13B-SuperHOT-8K-GPTQ](https://huggingface.co/TheBloke/Pygmalion-13B-SuperHOT-8K-GPTQ/tree/main)
* [Llama-2-7b-Chat-GPTQ](https://huggingface.co/TheBloke/Llama-2-7b-Chat-GPTQ)
* [pygmalion-6b](PygmalionAI/pygmalion-6b)

*TODO: implement Whisper AI*
### How to install
1. Create ```memories.json``` follow the ```memories-sample.json``` and add your name inside it.
2. Create folder name LLM ```models/LLM``` and put your local model inside LLM directory.
3. Create folder name TTS and vits ```models/TTS/vits``` and put your local VITS TTS model inside vits directory.
4. Create and activate python virtual environment ```python -m venv venv && source venv/bin/activate```
5. Install wheel package: ```pip install wheel```
5. Install PyTorch: ```pip install torch==2.0.0+cu117 torchaudio==2.0.1+cu117 torchvision==0.15.1+cu117 --extra-index-url https://download.pytorch.org/whl/cu117```
6. Install the requirements ```pip install -r requirements.txt```.
7. Add .env follow the .env-sample.
8. Add ```character.json``` follow ```character-sample.json``` or add your desirred character.
9. Run ```python main.py```

### Dotenv variables docs.

* ```MODEL_NAME_OR_PATH```
  - You must download the model manually and save it to the ```model/LLMS/``` folder. Model name from hub is not working for a moment.
  - ***PLEASE*** don't include any slashes like ```\``` or ```/``` otherwise the system will try to find and download the models from huggingface hub or maybe an ***error*** accured.
  - Example for local model: ```Pygmalion-6b``` or ```Pygmalion-13B-SuperHOT-8K-GPTQ```

* ```TEMPLATE_TYPE```  for changing the characteristic of the models.
  - ```pygmalion``` roleplay, specials for pygmalion models.
  - ```prompt``` for all models.

* ```MODEL_TYPE``` the model types.
  - ```GPTQ```
  - ```GGML```
  - ```SPLITTED```

* ```SPEAKER_ID``` go to [speakers.json](models/TTS/speakers.json) to see all the speaker_id

### Credits: 
* [CjangCjengh](https://github.com/CjangCjengh)
* [Francis-Komizu](https://github.com/Francis-Komizu)
* [ZoltanAI](https://github.com/ZoltanAI)
* [jllllll](https://github.com/jllllll)
* [Aqirito](https://github.com/Aqirito)
