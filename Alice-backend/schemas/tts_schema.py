from pydantic import BaseModel

class BaseTtsModel(BaseModel):
  tts_type: str
  language: str
  speed: float
  speaker_id: int
  voice: str
  pitch: str
  rate: str
  volume: str

class UpdateTtsModel(BaseTtsModel):
  pass