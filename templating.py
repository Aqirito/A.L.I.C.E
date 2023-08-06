import json
import os
from dotenv import dotenv_values
from prompting import build_prompt_for

# load ENV
env = dotenv_values(".env")
TEMPLATE_TYPE = env['TEMPLATE_TYPE']

current_path = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(current_path, "character.json"), "r") as f:
    f.seek(0)  # Move to the beginning of the file
    character = json.loads(f.read())
    
def setTemplate():
    if TEMPLATE_TYPE == "pygmalion":
        if len(character["history"]) == 0 and character["char_greeting"] is not None:
            print(f"{character['char_name']}: {character['char_greeting']}")
  
        template = build_prompt_for(history=character['history'],
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