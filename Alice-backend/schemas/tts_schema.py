from pydantic import BaseModel

class BaseTtsModel(BaseModel):
  """
  'voice': 'en-US-AnaNeural',
  'pitch': '+0Hz',
  'rate':'+0%',
  'volume': '+0%'
  EdgeTTS or MoeTTS
  """
  tts_type: str              # EdgeTTS, MoeTTS
  volume: str
  language: str              # [EN], [JA], [ZH], [KO] (MoeTTS)
  speed: float               # good results is 0.77
  speaker_id: int            # 607 (MoeTTS)
  voice: str                 # copy and paste one name in a list of voices from models/TTS/moe-tts-speaker.txt
  pitch: str
  rate: str
  volume: str

class UpdateTtsModel(BaseTtsModel):
  pass