import logging
from langchain import HuggingFacePipeline, PromptTemplate
from transformers import AutoTokenizer, AutoModelForCausalLM, AutoConfig
from accelerate import infer_auto_device_map, init_empty_weights
from auto_gptq import AutoGPTQForCausalLM
import torch
from dotenv import dotenv_values
import os
import glob

# load ENV
env = dotenv_values(".env")
MODEL_LOADER = env['MODEL_LOADER']

def loadModelAndTokenizer(model_name_or_path, model_basename):
    if MODEL_LOADER == "AutoGPTQ":
        return AutoGPTQLoader(model_name_or_path, model_basename)

    elif MODEL_LOADER == "HuggingFaceBig":
        return HuggingFaceBigLoader(model_name_or_path)
  
    elif MODEL_LOADER == "ExLlama":
        return ExLlamaLoader(model_name_or_path)
    else:
        raise Exception(
            "!!!!!No model type found!!!!! in {}".format(MODEL_LOADER)
        )
    
def HuggingFaceBigLoader(model_name_or_path):
    # config = AutoConfig.from_pretrained(model_name_or_path)
    # with init_empty_weights():
    #     model = AutoModelForCausalLM.from_config(config)

    # device_map = infer_auto_device_map(model, no_split_module_classes=["GPTJBlock"])
    # device_map["transformer.h.27"] = "disk"
    tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, use_fast=True, return_tensors="pt")
    model = AutoModelForCausalLM.from_pretrained(
        model_name_or_path,
        device_map="auto",
        torch_dtype="auto"
        )
    return {
        "tokenizer": tokenizer,
        "model": model
    }
    
def AutoGPTQLoader(model_name_or_path, model_basename):
    tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, use_fast=True)
    model = AutoGPTQForCausalLM.from_quantized(
        model_name_or_path,
        model_basename=model_basename,
        use_safetensors=True,
        # trust_remote_code=True,
        device_map='auto',
        use_triton=False,
        load_in_8bit=True,
        # use_auth_token=True,
        device="cuda"
        )
    model.seqlen = 4096

    return {
        "model": model,
        "tokenizer": tokenizer
    }


def ExLlamaLoader(model_name_or_path):
    # from init_models import loadModelAndTokenizer
    from exllama.model import ExLlama, ExLlamaCache, ExLlamaConfig
    from exllama.tokenizer import ExLlamaTokenizer
    from exllama.generator import ExLlamaGenerator

    tokenizer_path = os.path.join(model_name_or_path, "tokenizer.model")
    model_config_path = os.path.join(model_name_or_path, "config.json")
    st_pattern = os.path.join(model_name_or_path, "*.safetensors")
    model_path = glob.glob(st_pattern)[0]


    # Create config, model, tokenizer and generator
    config = ExLlamaConfig(model_config_path)               # create config from config.json
    config.model_path = model_path                          # supply path to model weights file

    model = ExLlama(config)                                 # create ExLlama instance and load the weights
    tokenizer = ExLlamaTokenizer(tokenizer_path)            # create tokenizer from tokenizer model file

    return {
        "model": model,
        "tokenizer": tokenizer
    }

            