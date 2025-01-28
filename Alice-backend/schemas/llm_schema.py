from pydantic import BaseModel

class BaseModelLoader(BaseModel):
    temperature: float
    max_length: int
    max_new_tokens: int
    top_k: int
    top_p: float
    typical_p: float
    repetition_penalty: float
    penalty_alpha: float
    do_sample: bool
    
class ExllamaCfg(BaseModelLoader):
    min_p: float                                   # Do not consider tokens with probability less than this
    typical: float                                  # Locally typical sampling threshold, 0.0 to disable typical sampling
    token_repetition_penalty_max: float            # Repetition penalty for most recent tokens
    token_repetition_penalty_sustain: int          # No. most recent tokens to repeat penalty for, -1 to apply to whole context
    token_repetition_penalty_decay: int            # Gradually decrease penalty over this many tokens
    beams: int
    beam_length: int

class UpdateLlm(ExllamaCfg):
    pass