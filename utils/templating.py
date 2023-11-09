import json
import os
# from dotenv import dotenv_values
from .prompting import build_prompt_for

project_path = os.path.abspath(os.getcwd())




# # load ENV
# env = dotenv_values(".env")

current_path = os.path.dirname(os.path.realpath(__file__))
    
def setTemplate():
    global llm_loader_settings
    
    # inside setTemplate to reload the character everytime
    with open(os.path.join(project_path, "configs/llm_loader_settings.json"), "r") as f:
        f.seek(0)  # Move to the beginning of the file
        llm_loader_settings = json.loads(f.read())
        TEMPLATE_TYPE = llm_loader_settings['template_type']

    # inside setTemplate to reload the character everytime
    with open(os.path.join(project_path, "configs/character.json"), "r", encoding='utf-8') as f:
        f.seek(0)  # Move to the beginning of the file
        character = json.loads(f.read())

    # inside setTemplate to reload the memories everytime
    with open(os.path.join(project_path, "configs/memories.json"), "r", encoding='utf-8') as f:
        f.seek(0)  # Move to the beginning of the file
        memories = json.loads(f.read())
  
    if TEMPLATE_TYPE == "pygmalion":
        template = build_prompt_for(history=memories['history'],
                              user_message='{question}',
                              char_name=character['char_name'],
                              char_persona=character['char_persona'],
                              example_dialogue=character['example_dialogue'],
                              world_scenario=character['world_scenario'])
        
        return template

    elif TEMPLATE_TYPE == "prompt":
        # template = """Question: {question}

        # Answer: Let's think step by step."""

        template = """Question: {question}

        Answer: Let's reply quickly"""

        return template
    
    else:
        raise Exception(
            "Template Not Found")