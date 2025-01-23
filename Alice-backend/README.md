
# A.L.I.C.E PROJECT

A.L.I.C.E (Artificial Labile Intelligence Cybernated Existence)

Is a REST API of an A.I companions.

### My specs:
* Nvidia RTX 3060 12 GB
* Intel i5 12400
* 24 GB DDR4 RAM
* OS: Ubuntu 24.04 LTS

*This work only for `Llama GPTQ` and `GPTJ splitted` model for now.*

*I will add type GGML model soon.*

### Model tested:
* [TheBloke/Pygmalion-13B-SuperHOT-8K-GPTQ](https://huggingface.co/TheBloke/Pygmalion-13B-SuperHOT-8K-GPTQ/tree/main)
* [Llama-2-7b-Chat-GPTQ](https://huggingface.co/TheBloke/Llama-2-7b-Chat-GPTQ)
* [pygmalion-6b](PygmalionAI/pygmalion-6b)

### Preqrequisites
* Python 3.10.9
* CUDA 12.4

### How to run
1. Clone this repository ```git clone https://github.com/Aqirito/A.L.I.C.E.git``` and go to the project folder.
2. Install CUDA 12 ```sudo apt install nvidia-cuda-toolkit``` will install the latest version of CUDA. for Ubuntu 24.04 LTS it's version 12
1. Inside ```/configs``` folder, Make a copy of all ```*-sample.json```file and rename by remove the ```-sample```.
2. Download your LLM models and put your local model inside ```models/LLM``` folder.
3. [MoeTTS](https://github.com/CjangCjengh/TTSModels#japanese--english--korean--chinese) model Download your VITS models and put your local VITS TTS model inside ```models/TTS/vits``` folder.
4. Create and activate python virtual environment ```python -m venv env && source env/bin/activate```
5. Install wheel package: ```pip install wheel```
6. Install the requirements ```pip install -r requirements.txt```
7. Install Exllama ```python -m pip install git+https://github.com/jllllll/exllama```
8. Add .env follow the .env-sample and change the value ```cp .env-sample .env```
9. Run ```uvicorn fast:app``` and go to ```localhost:8000/docs``` to access the Swagger UI.

### Dotenv variables docs
* ```MODEL_NAME_OR_PATH```
  - You must download the model manually and save it to the ```model/LLMS/``` folder. Model name from hub is not working for a moment.
  - ***PLEASE*** don't include any slashes like ```\``` or ```/``` otherwise the system will try to find and download the models from huggingface hub or maybe an ***error*** accured.
  - Example for local model: ```Pygmalion-6b``` or ```Pygmalion-13B-SuperHOT-8K-GPTQ```

### LLM loader settings docs
* ```TEMPLATE_TYPE```  For changing the characteristic of the models.
  - `pygmalion` Roleplay, specials for pygmalion models.
  - `prompt` For all models basically just a normal AI chat bot.

* ```MODEL_LOADER```  A model loader for the LLM model.
  - `AutoGPTQ` AutoGPTQ model loader (GPTQ type only).
  - `HuggingFaceBig` HuggingFace Big model loader (more than one .safetensors file).
  - `ExLlama` Exllama model loader. use this for faster response. (GPTQ type only)


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