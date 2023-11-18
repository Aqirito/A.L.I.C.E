
# LangPlusWaifu REST API

A REST API of an AI chatbot

*Tested in Windows with Pytorch 2.0.0 with CUDA 11.7*
*Python 3.10*
*pip 23.2.1*
*langchain 0.0.245*

### My specs:
* Nvidia RTX 3060 12 GB
* Intel i5 12400

*This work only for Llama type GPTQ model for now.*

*I will add type GGML model soon.*

*the default voice is from character named Kamisato ayaka from video game called Genshin Impact.*

Model tested:
* [TheBloke/Pygmalion-13B-SuperHOT-8K-GPTQ](https://huggingface.co/TheBloke/Pygmalion-13B-SuperHOT-8K-GPTQ/tree/main)
* [Llama-2-7b-Chat-GPTQ](https://huggingface.co/TheBloke/Llama-2-7b-Chat-GPTQ)
* [pygmalion-6b](PygmalionAI/pygmalion-6b)


### How to run
1. Inside ```/configs``` folder, Make a copy of all ```*-sample.json```file and rename by remove the ```-sample```.
2. Download your LLM models and put your local model inside ```models/LLM``` folder.
3. *(optional if you want to use [MoeTTS](https://github.com/CjangCjengh/TTSModels#japanese--english--korean--chinese) model)* Download your VITS models and put your local VITS TTS model inside ```models/TTS/vits``` folder.
4. Create and activate python virtual environment ```python -m venv venv && source venv/bin/activate```
5. Install wheel package: ```pip install wheel```
5. Install PyTorch: ```pip install torch==2.0.0+cu117 torchaudio==2.0.1+cu117 torchvision==0.15.1+cu117 --extra-index-url https://download.pytorch.org/whl/cu117```
6. Install the requirements ```pip install -r requirements.txt```.
7. Add .env follow the .env-sample.
9. Run ```uvicorn fast:app``` and go to ```localhost:8000/docs``` to access the Swagger UI.

### Dotenv variables docs.

* ```MODEL_NAME_OR_PATH```
  - You must download the model manually and save it to the ```model/LLMS/``` folder. Model name from hub is not working for a moment.
  - ***PLEASE*** don't include any slashes like ```\``` or ```/``` otherwise the system will try to find and download the models from huggingface hub or maybe an ***error*** accured.
  - Example for local model: ```Pygmalion-6b``` or ```Pygmalion-13B-SuperHOT-8K-GPTQ```

### LLM loader settings docs.

* ```TEMPLATE_TYPE```  For changing the characteristic of the models.
  - ```pygmalion``` Roleplay, specials for pygmalion models.
  - ```prompt``` For all models basically just a normal AI chat bot.

* ```MODEL_TYPE``` The model types.
  - ```GPTQ```     Quantized models for consumer grade GPU like me 😝.
  - ```GGML```     CPU based models
  - ```SPLITTED``` Multiple .safetensors file

* ```MODEL_LOADER``` AutoGPTQ, HuggingFaceBig or ExLlama


### LLM settings
* Base model config
  - [Hugging Face Local Pipelines](https://python.langchain.com/docs/integrations/llms/huggingface_pipelines)
  - [Hugging Face Transformers Pipelines](https://huggingface.co/docs/transformers/v4.35.2/en/main_classes/pipelines#pipelines)

* Exllama model config
  - See examples of [Exllama](https://github.com/jllllll/exllama)

### TTS settings

* ```tts_type``` Type of the TTS model used.
  - `EdgeTTS` [edge-tts](https://github.com/rany2/edge-tts) only support english.
  - `MoeTTS` [moe-tts](https://github.com/CjangCjengh/TTSModels#japanese--english--korean--chinese)

* ```language``` The language of TTS (moe-tts)
  - `[EN]` English
  - `[JA]` Japanese
  - `[ZH]` Chinese
  - `[KO]` Korean

* ```speed``` Speed of the TTS speaker (moe-tts)
* ```speaker_id``` Go to [speakers.json](models/TTS/speakers.json) to see all the speaker_id (moe-tts)
* ```voice``` Can search speaker from [edge-tts](https://github.com/rany2/edge-tts)
* ```pitch``` The pitch voice of the speaker (edge-tts)
* ```rate``` Speed of the speaker (edge-tts)
* ```volume``` Volume of the speaker (edge-tts)

### Credits: 
* [CjangCjengh](https://github.com/CjangCjengh) Author of moe-tts.
* [ZoltanAI](https://github.com/ZoltanAI) Author of AI character editor.
* [turboderp](https://github.com/turboderp) Author of Exllama.
* [jllllll](https://github.com/jllllll) Makes Python module for Exllama.