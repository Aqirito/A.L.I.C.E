from init_models import loadModelAndTokenizer

model_name_or_path = "TheBloke/Llama-2-7b-Chat-GPTQ"
model_basename = "gptq_model-4bit-128g"
dd = loadModelAndTokenizer(model_name_or_path=model_name_or_path, model_basename=model_basename)
print(dd)