from pydantic import BaseModel

class SystemSchema(BaseModel):
    template_type: str         # for now is 'pygmalion' and 'prompt'
    model_type: str            # GPTQ
    model_loader: str          # AutoGPTQ, HuggingFaceBig, ExLlama
    language: str              # [EN], [JA], [ZH], [KO]
    speed: float               # good results is 0.77
    speaker_id: int            # 607