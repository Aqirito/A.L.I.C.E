from transformers import logging, AutoTokenizer
from auto_gptq import AutoGPTQForCausalLM

def checkModelType(model_name_or_path):
    model_type = ""
    is_model_type = model_name_or_path.upper()
    if "GPTQ" in is_model_type:
        model_type = "GPTQ"
        return model_type
    if "GGML" in is_model_type:
        model_type = "GGML"
        return model_type
    return model_type

def loadModelAndTokenizer(model_name_or_path, model_basename):
    model_type = checkModelType(model_name_or_path)

    if model_type == "GPTQ":
        tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, use_fast=True)
        model = AutoGPTQForCausalLM.from_quantized(
            model_name_or_path,
            model_basename=model_basename,
            use_safetensors=True,
            trust_remote_code=True,
            device_map='auto',
            use_triton=False,
            load_in_4bit=True,
            quantize_config=None)
        model.seqlen = 4096


        return {
            "tokenizer": tokenizer,
            "model": model
        }
    else:
        return {
            "tokenizer": None,
            "model": None
        }
            