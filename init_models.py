from transformers import AutoTokenizer, AutoModelForCausalLM, AutoConfig
from accelerate import infer_auto_device_map, init_empty_weights
from auto_gptq import AutoGPTQForCausalLM
import torch

def checkModelType(model_name_or_path):
    model_type = None
    is_model_type = model_name_or_path.upper()
    if "GPTQ" in is_model_type:
        model_type = "GPTQ"
        return model_type
    elif "GGML" in is_model_type:
        model_type = "GGML"
        return model_type
    else:
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
            load_in_8bit=True,
            quantize_config=None)
        model.seqlen = 4096


        return {
            "tokenizer": tokenizer,
            "model": model
        }
    elif model_type is None:
        print("No model type found", model_name_or_path)
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
        return {
            "tokenizer": None,
            "model": None
        }
            