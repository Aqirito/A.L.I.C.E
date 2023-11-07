import base64
from langchain import PromptTemplate, LLMChain
from langchain import HuggingFacePipeline
from transformers import logging
from dotenv import dotenv_values
from utils.init_models import loadModelAndTokenizer
import json
import os
from utils.templating import setTemplate
from moe.main import synthesize
from exllama.model import ExLlamaCache
from exllama.generator import ExLlamaGenerator
import os
import glob


from typing import Union
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from schemas import ExllamaCfg, UpdateLlm, SystemSchema, ChatModel

app = FastAPI()

current_path = os.path.dirname(os.path.realpath(__file__))
project_path = os.path.abspath(os.getcwd())

with open(os.path.join(project_path, "configs/system_cfg.json"), "r") as f:
    f.seek(0)  # Move to the beginning of the file
    system_cfg = json.loads(f.read())

# # load ENV
env = dotenv_values(".env")

MODEL_NAME_OR_PATH = env['MODEL_NAME_OR_PATH']
MODEL_TYPE = system_cfg['model_type']
MODEL_LOADER = system_cfg['model_loader']
LANGUAGE = system_cfg['language']
SPEED = system_cfg['speed']
SPEAKER_ID = system_cfg['speaker_id']

if "/" not in MODEL_NAME_OR_PATH:
    MODEL_NAME_OR_PATH = os.path.abspath(os.path.join("models/LLM", MODEL_NAME_OR_PATH))

st_pattern = os.path.join(MODEL_NAME_OR_PATH, "*.safetensors")
try:
    MODEL_BASENAME = glob.glob(st_pattern)[0] # find all files in the directory that match the * pattern
except:
    MODEL_BASENAME=None


init_model = loadModelAndTokenizer(model_name_or_path=MODEL_NAME_OR_PATH, model_basename=MODEL_BASENAME)
# init_model = ""

model = init_model["model"]
tokenizer = init_model["tokenizer"]

with open(os.path.join(project_path, "configs/character.json"), "r") as f:
    f.seek(0)  # Move to the beginning of the file
    character = json.loads(f.read())

with open(os.path.join(project_path, "configs/memories.json"), "r") as f:
    f.seek(0)  # Move to the beginning of the file
    memories = json.loads(f.read())

with open(os.path.join(project_path, "configs/llm_loader_cfg.json"), "r") as f:
    f.seek(0)  # Move to the beginning of the file
    llm_loader_cfg = json.loads(f.read())

def saveReply(question, bot_response):
    
    replace_name_reply = bot_response.replace('<USER>', memories['MC_name'])
    print(f"{character['char_name']}:{replace_name_reply}")

    # Insert the chat history
    memories['history'].append(f"You: {question}")
    memories['history'].append(f"{character['char_name']}:{replace_name_reply}")

    # Save the chat history to a JSON file
    with open(os.path.join(project_path, "configs/memories.json"), "w", encoding='utf-8') as outfile:
        json.dump(memories, outfile, ensure_ascii=False, indent=2)

    synthesize(text=LANGUAGE+replace_name_reply+LANGUAGE, speed=float(SPEED), out_path="reply.wav", speaker_id=int(SPEAKER_ID))


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/chat")
def chat(ChatModel: ChatModel):
    if MODEL_TYPE == "GPTQ":
        if MODEL_LOADER == "AutoGPTQ":
            model.seqlen = 4096
            # Prevent printing spurious transformers error when using pipeline with AutoGPTQ
            logging.set_verbosity(logging.CRITICAL)

            pipeline = pipeline(
                "text-generation",
                model=model,
                tokenizer=tokenizer,
                max_length=int(llm_loader_cfg['max_length']),
                max_new_tokens=int(llm_loader_cfg['max_new_tokens']),
                temperature=float(llm_loader_cfg['temperature']),
                top_p=float(llm_loader_cfg['top_p']),
                typical_p=float(llm_loader_cfg['typical_p']),
                repetition_penalty=float(llm_loader_cfg['repetition_penalty']),
                penalty_alpha=float(llm_loader_cfg['penalty_alpha']),
                do_sample=float(llm_loader_cfg['do_sample'])
            )
            llm = HuggingFacePipeline(pipeline=pipeline)

            question = ChatModel.questions
            
            template = setTemplate() # set and execute the right template of the models

            # prompt = PromptTemplate(template=template, input_variables=["question"]) # generate the prompt
            prompt = PromptTemplate.from_template(template)
            prompt.format(question=question)

            # using pipeline from Langchain
            llm_chain = LLMChain(prompt=prompt, llm=llm) # create a chain
            bot_reply = llm_chain.run(question) # run the chain

            # saveReply(question, bot_reply)
            replace_name_reply = str(bot_reply).replace('<USER>', memories['MC_name'])

            answer = f"{character['char_name']}:{replace_name_reply}"

            # Insert the chat history
            memories['history'].append(f"You: {question}")
            memories['history'].append(f"{character['char_name']}:{replace_name_reply}")

            # Save the chat history to a JSON file
            with open(os.path.join(project_path, "configs/memories.json"), "w", encoding='utf-8') as outfile:
                json.dump(memories, outfile, ensure_ascii=False, indent=2)

            synthesize(text=LANGUAGE+replace_name_reply+LANGUAGE, speed=float(SPEED), out_path="reply.wav", speaker_id=int(SPEAKER_ID))
            file_path = os.path.join(project_path, "reply.wav")

            try:
                with open(file_path, "rb") as audio_file:
                    audio_content = base64.b64encode(audio_file.read()).decode("utf-8")

                response_data = {
                    "question": question,
                    "reply_text": answer,
                    "reply_audio": audio_content
                }
                return JSONResponse(content=response_data)
            except FileNotFoundError:
                raise HTTPException(status_code=404, detail="File not found")
            
        elif MODEL_LOADER == "ExLlama":
            # create cache for inference
            cache = ExLlamaCache(model)
            generator = ExLlamaGenerator(model, tokenizer, cache)   # create generator

            # Configure generator
            # generator.disallow_tokens([tokenizer.eos_token_id])
            generator.settings.token_repetition_penalty_max = float(llm_loader_cfg['token_repetition_penalty_max'])
            generator.settings.temperature = float(llm_loader_cfg['temperature'])
            generator.settings.top_p = float(llm_loader_cfg['top_p'])
            generator.settings.top_k = int(llm_loader_cfg['top_k'])
            generator.settings.typical = float(llm_loader_cfg['typical'])
            generator.settings.beams = int(llm_loader_cfg['beams'])
            generator.settings.beam_length = int(llm_loader_cfg['beam_length'])
            generator.settings.token_repetition_penalty_sustain = int(llm_loader_cfg['token_repetition_penalty_sustain'])
            generator.settings.token_repetition_penalty_decay = int(llm_loader_cfg['token_repetition_penalty_decay'])

            question = ChatModel.questions
            template = setTemplate() # set and execute the right template of the models
            prompt = template.format(question=question)

            output = generator.generate_simple(prompt, max_new_tokens=int(llm_loader_cfg['max_new_tokens']))

            replace_name_reply = str(output[len(prompt):]).replace('<USER>', memories['MC_name'])

            answer = f"{character['char_name']}:{replace_name_reply}"

            # Insert the chat history
            memories['history'].append(f"You: {question}")
            memories['history'].append(f"{character['char_name']}:{replace_name_reply}")

            # Save the chat history to a JSON file
            with open(os.path.join(project_path, "configs/memories.json"), "w", encoding='utf-8') as outfile:
                json.dump(memories, outfile, ensure_ascii=False, indent=2)

            synthesize(text=LANGUAGE+replace_name_reply+LANGUAGE, speed=float(SPEED), out_path="reply.wav", speaker_id=int(SPEAKER_ID))
            file_path = os.path.join(project_path, "reply.wav")

            try:
                with open(file_path, "rb") as audio_file:
                    audio_content = base64.b64encode(audio_file.read()).decode("utf-8")

                response_data = {
                    "question": question,
                    "reply_text": answer,
                    "reply_audio": audio_content
                }

                return JSONResponse(content=response_data)
            except FileNotFoundError:
                raise HTTPException(status_code=404, detail="File not found")
    else:
        raise HTTPException(status_code=404, detail=f"Model Type Not Found: {MODEL_TYPE}")


@app.get("/setings/llm_loader")
def llm_loader():
    return llm_loader_cfg

@app.put("/setings/llm_loader", response_model=UpdateLlm)
def llm_loader(llm: UpdateLlm):
    with open(os.path.join(project_path, "configs/llm_loader_cfg.json"), "w", encoding='utf-8') as outfile:
        json.dump(json.loads(llm.json()), outfile, ensure_ascii=False, indent=2)
    return llm

@app.get("/setings/system")
def system_settings():
    return system_cfg

@app.put("/setings/system", response_model=SystemSchema)
def system_settings(system: SystemSchema):
    """
    template_type: # for now is 'pygmalion' and 'prompt'
    model_type: # GPTQ
    model_loader: # AutoGPTQ, HuggingFaceBig, ExLlama
    language: # [EN], [JA], [ZH], [KO]
    speed: float # good results is 0.77
    speaker_id: int # 607
    """
    
    with open(os.path.join(project_path, "configs/system_cfg.json"), "w", encoding='utf-8') as outfile:
        json.dump(json.loads(system.json()), outfile, ensure_ascii=False, indent=2)
    return system

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
