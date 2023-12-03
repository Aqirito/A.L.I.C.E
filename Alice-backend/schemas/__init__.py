from pydantic import BaseModel
from .llm_schema import BaseModelLoader, ExllamaCfg, UpdateLlm
from .system_schema import SystemSchema
from.tts_schema import BaseTtsModel, UpdateTtsModel

class ChatModel(BaseModel):
    questions: str