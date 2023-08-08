# from init_models import loadModelAndTokenizer
from exllama.model import ExLlama, ExLlamaCache, ExLlamaConfig
from exllama.tokenizer import ExLlamaTokenizer
from exllama.generator import ExLlamaGenerator
import os
import glob

model_directory =  "D:\playground\langPlusWaifu\models\LLM\Llama-2-7b-Chat-GPTQ"

# Locate files we need within that directory

tokenizer_path = os.path.join(model_directory, "tokenizer.model")
model_config_path = os.path.join(model_directory, "config.json")
st_pattern = os.path.join(model_directory, "*.safetensors")
model_path = glob.glob(st_pattern)[0]

# Create config, model, tokenizer and generator

config = ExLlamaConfig(model_config_path)               # create config from config.json
config.model_path = model_path                          # supply path to model weights file

model = ExLlama(config)                                 # create ExLlama instance and load the weights
tokenizer = ExLlamaTokenizer(tokenizer_path)            # create tokenizer from tokenizer model file

cache = ExLlamaCache(model)                             # create cache for inference
generator = ExLlamaGenerator(model, tokenizer, cache)   # create generator

# Configure generator

generator.disallow_tokens([tokenizer.eos_token_id])

generator.settings.token_repetition_penalty_max = 1.2
generator.settings.temperature = 0.95
generator.settings.top_p = 0.65
generator.settings.top_k = 100
generator.settings.typical = 0.5

# Produce a simple generation

prompt = """
Questions: what is the capital city of Malaysia?
Answers: Lets anwser it quickly! 
"""
# print (prompt, end = "")

output = generator.generate_simple(prompt, max_new_tokens = 200)

print(output[len(prompt):])