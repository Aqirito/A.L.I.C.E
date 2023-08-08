from langchain import PromptTemplate, LLMChain
from langchain import HuggingFacePipeline
from transformers import pipeline, logging
from dotenv import dotenv_values
from init_models import loadModelAndTokenizer
import json
import os
from templating import setTemplate
from moe.main import synthesize
from exllama.model import ExLlamaCache
from exllama.generator import ExLlamaGenerator
import os
import glob

# load ENV
env = dotenv_values(".env")
MODEL_NAME_OR_PATH = env['MODEL_NAME_OR_PATH']
MODEL_TYPE = env['MODEL_TYPE']
MODEL_LOADER = env['MODEL_LOADER']
LANGUAGE = env['LANGUAGE']
SPEED = env['SPEED']
SPEAKER_ID = env['SPEAKER_ID']

if "/" not in MODEL_NAME_OR_PATH:
    MODEL_NAME_OR_PATH = os.path.abspath(os.path.join("models/LLM", MODEL_NAME_OR_PATH))

st_pattern = os.path.join(MODEL_NAME_OR_PATH, "*.safetensors")
try:
    MODEL_BASENAME = glob.glob(st_pattern)[0] # find all files in the directory that match the * pattern
except:
    MODEL_BASENAME=None

current_path = os.path.dirname(os.path.realpath(__file__))
init_model = loadModelAndTokenizer(model_name_or_path=MODEL_NAME_OR_PATH, model_basename=MODEL_BASENAME)

model = init_model["model"]
tokenizer = init_model["tokenizer"]

with open(os.path.join(current_path, "character.json"), "r") as f:
    f.seek(0)  # Move to the beginning of the file
    character = json.loads(f.read())

with open(os.path.join(current_path, "memories.json"), "r") as f:
    f.seek(0)  # Move to the beginning of the file
    memories = json.loads(f.read())


def saveReply(question, bot_response):
    
    replace_name_reply = bot_response.replace('<USER>', memories['MC_name'])
    print(f"{character['char_name']}:{replace_name_reply}")

    # Insert the chat history
    memories['history'].append(f"You: {question}")
    memories['history'].append(f"{character['char_name']}:{replace_name_reply}")

    # Save the chat history to a JSON file
    with open(os.path.join(current_path, "memories.json"), "w", encoding='utf-8') as outfile:
        json.dump(memories, outfile, ensure_ascii=False, indent=2)

    synthesize(text=LANGUAGE+replace_name_reply+LANGUAGE, speed=float(SPEED), out_path="reply.wav", speaker_id=int(SPEAKER_ID))

if MODEL_TYPE == "GPTQ":
    if MODEL_LOADER == "AutoGPTQ":
        model.seqlen = 4096
        # Prevent printing spurious transformers error when using pipeline with AutoGPTQ
        logging.set_verbosity(logging.CRITICAL)

        pipeline = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            max_length=int(env['max_length']),
            max_new_tokens=int(env['max_new_tokens']),
            temperature=float(env['temperature']),
            top_p=float(env['top_p']),
            typical_p=float(env['typical_p']),
            repetition_penalty=float(env['repetition_penalty']),
            penalty_alpha=float(env['penalty_alpha']),
            do_sample=float(env['do_sample'])
        )
        llm = HuggingFacePipeline(pipeline=pipeline)

        while True:
            question = input("You: ")
            
            template = setTemplate() # set and execute the right template of the models

            # prompt = PromptTemplate(template=template, input_variables=["question"]) # generate the prompt
            prompt = PromptTemplate.from_template(template)
            prompt.format(question=question)

            # using pipeline from Langchain
            llm_chain = LLMChain(prompt=prompt, llm=llm) # create a chain
            bot_reply = llm_chain.run(question) # run the chain

            saveReply(question, bot_reply)

    elif MODEL_LOADER == "ExLlama":
        # create cache for inference
        cache = ExLlamaCache(model)
        generator = ExLlamaGenerator(model, tokenizer, cache)   # create generator

        # Configure generator
        # generator.disallow_tokens([tokenizer.eos_token_id])
        generator.settings.token_repetition_penalty_max = float(env['token_repetition_penalty_max'])
        generator.settings.temperature = float(env['temperature'])
        generator.settings.top_p = float(env['top_p'])
        generator.settings.top_k = int(env['top_k'])
        generator.settings.typical = float(env['typical'])
        generator.settings.beams = int(env['beams'])
        generator.settings.beam_length = int(env['beam_length'])
        generator.settings.token_repetition_penalty_sustain = int(env['token_repetition_penalty_sustain'])
        generator.settings.token_repetition_penalty_decay = int(env['token_repetition_penalty_decay'])


        while True:
            question = input("You: ")
            template = setTemplate() # set and execute the right template of the models
            prompt = template.format(question=question)

            output = generator.generate_simple(prompt, max_new_tokens=int(env['max_new_tokens']))

            saveReply(question, str(output[len(prompt):]))
else:
    raise Exception(
        "Model Type Not Found: ", MODEL_TYPE)

