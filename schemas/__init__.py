from pydantic import BaseModel
from .llm_schema import BaseModelLoader, ExllamaCfg, UpdateLlm
from .system_schema import SystemSchema

class ChatModel(BaseModel):
    questions: str