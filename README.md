
# LangPlusWaifu
*CUDA 11.7*
*Python 3.10*
*pip 23.2.1*
*Tested with langchain 0.0.245*

*This work only for type GPTQ model for now.*

*I will add type GGML model soon.*

*the default voice is from character named Kamisato Yayaka from video game called Genshin Impact.*

***TODO prevent chat from auto generating by itself***

1. Create python virtual environment ```python -m venv venv && source venv/bin/activate```.
2. Install the requirements ```pip install -r requirements.txt```.
3. Add .env follow the .env-sample.
4. Add ```character.json``` follow ```character-sample.json``` or add your desirred character.
5. Run ```python main.py```.

#### Dotenv variables docs.

* ```MODEL_NAME_OR_PATH```
  - For local models: ***PLEASE*** don't include any slashes like ```\``` or ```/``` otherwise the system will try to find and download the models from huggingface hub.
  - Example for huggingface hub: ```username/models-GPTQ-or-GGML```
  - Example for local model: ```Pygmalion-6b```
  
* ```MODEL_BASENAME```
  - the .safetensors file name inside the model directories". don't include the after the ```.safetensors``` or ```.bin``` of the file
  - this only for GPTQ models
  - empty string for non-GPTQ model

* ```TEMPLATE_TYPE```  for changing the characteristic of the models.
  - ```pygmalion``` roleplay, specials for pygmalion models.
  - ```prompt``` for all models.

* ```MODEL_TYPE``` the model types.
  - ```GPTQ```
  - ```GGML```
  - ```SPLITTED```

#### Credits: 
* [CjangCjengh](https://github.com/CjangCjengh)
* [Francis-Komizu](https://github.com/Francis-Komizu)
* [ZoltanAI](https://github.com/ZoltanAI)
* [Aqirito](https://github.com/Aqirito)
