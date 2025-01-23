from pydantic import BaseModel

class SystemSchema(BaseModel):
    template_type: str         # for now is 'pygmalion' and 'prompt'
    model_loader: str          # AutoGPTQ, HuggingFaceBig, ExLlama