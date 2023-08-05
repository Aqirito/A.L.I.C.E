from langchain import PromptTemplate, LLMChain
from langchain import HuggingFacePipeline
from transformers import pipeline, logging
from dotenv import dotenv_values
from init_models import loadModelAndTokenizer
import json
import os
from templating import setTemplate

# load ENV
env = dotenv_values(".env")
HUGGINGFACEHUB_API_TOKEN = env['HUGGINGFACEHUB_API_TOKEN']
MODEL_NAME_OR_PATH = env['MODEL_NAME_OR_PATH']
MODEL_BASENAME = env['MODEL_BASENAME']
LOCAL_FILE_PATH = os.path.abspath(os.path.join("models", MODEL_NAME_OR_PATH))

current_path = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(current_path, "character.json"), "r") as f:
    f.seek(0)  # Move to the beginning of the file
    character = json.loads(f.read())

if len(character["history"]) == 0 and character["char_greeting"] is not None:
    print(f"{character['char_name']}: {character['char_greeting']}")

# TODO change dynamicly between local models and cached models
loadModelAndTokenizer = loadModelAndTokenizer(model_name_or_path=MODEL_NAME_OR_PATH, model_basename=MODEL_BASENAME)

model = loadModelAndTokenizer["model"]
tokenizer = loadModelAndTokenizer["tokenizer"]

model.seqlen = 4096

# Prevent printing spurious transformers error when using pipeline with AutoGPTQ
logging.set_verbosity(logging.CRITICAL)

pipeline = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_length=128,
    max_new_tokens=128,
    temperature=0.7,
    top_p=0.4,
    typical_p=0.2,
    repetition_penalty=1.15,
    penalty_alpha=0.6,
    do_sample=True
)
llm = HuggingFacePipeline(pipeline=pipeline)

template = setTemplate() # set the right template of the models
prompt = PromptTemplate(template=template, input_variables=["question"]) # generate the prompt

while True:
    question = input("You: ")

    llm_chain = LLMChain(prompt=prompt, llm=llm) # create a chain
    bot_reply = llm_chain.run(question) # run the chain

    replace_name = bot_reply.replace('<USER>', character['user_name'])

    print(replace_name)

    # Insert the chat history
    character['history'].append(f"You: {question}")
    character['history'].append(f"{character['char_name']}:{replace_name}")

    # Save the chat history to a JSON file
    with open(os.path.join(current_path, "character.json"), "w") as outfile:
        json.dump(character, outfile)