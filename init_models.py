from transformers import AutoTokenizer, AutoModelForCausalLM, AutoConfig
from accelerate import infer_auto_device_map, init_empty_weights
from auto_gptq import AutoGPTQForCausalLM
import torch
from dotenv import dotenv_values

# load ENV
env = dotenv_values(".env")
MODEL_TYPE = env['MODEL_TYPE']

def loadModelAndTokenizer(model_name_or_path, model_basename):
    if MODEL_TYPE == "GPTQ":
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
            "tokenizer": tokenizer,
            "model": model
        }
    elif MODEL_TYPE == "SPLITTED":
        config = AutoConfig.from_pretrained(model_name_or_path)
        with init_empty_weights():
            model = AutoModelForCausalLM.from_config(config)

        device_map = infer_auto_device_map(model, no_split_module_classes=["GPTJBlock"])
        device_map["transformer.h.27"] = "disk"
        print(device_map)
        tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, use_fast=True)
        model = AutoModelForCausalLM.from_pretrained(
            model_name_or_path,
            device_map=device_map,
            offload_folder="offload",
            offload_state_dict = True,
            low_cpu_mem_usage=True,
            torch_dtype=torch.float16)
        return {
            "tokenizer": tokenizer,
            "model": model
        }
    else:
        print("!!!!!No model type found!!!!!", MODEL_TYPE)
        return {
            "tokenizer": None,
            "model": None
        }
            