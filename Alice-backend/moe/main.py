import os
import json
import re
import sys
import torch
from torch import no_grad, LongTensor
from . import utils
from . import commons
from scipy.io.wavfile import write
from . models import SynthesizerTrn
from . text import text_to_sequence
current_path = os.path.abspath(os.getcwd())
project_path =os.path.dirname(os.getcwd())

model_info = os.path.join(current_path + "/models/TTS", "info.json")
model = os.path.join(current_path + "/models/TTS", "vits/model.pth")
model_config = os.path.join(current_path + "/models/TTS", "vits/config.json")
current_path = os.path.dirname(os.path.realpath(__file__))

# with open(os.path.join(current_path, "speakers.json"), "r", encoding='utf-8') as f:
#     f.seek(0)  # Move to the beginning of the file
#     J_speakers = json.loads(f.read())

def ex_print(text, escape=False):
    if escape:
        print(text.encode('unicode_escape').decode())
    else:
        print(text)

def get_label_value(text, label, default, warning_name='value'):
    value = re.search(rf'\[{label}=(.+?)\]', text)
    if value:
        try:
            text = re.sub(rf'\[{label}=(.+?)\]', '', text, 1)
            value = float(value.group(1))
        except:
            print(f'Invalid {warning_name}!')
            sys.exit(1)
    else:
        value = default
    return value, text

def get_label(text, label):
    if f'[{label}]' in text:
        return True, text.replace(f'[{label}]', '')
    else:
        return False, text
    
def get_text(text, hps, cleaned=False):
    if cleaned:
        text_norm = text_to_sequence(text, hps.symbols, [])
    else:
        text_norm = text_to_sequence(text, hps.symbols, hps.data.text_cleaners)
    if hps.data.add_blank:
        text_norm = commons.intersperse(text_norm, 0)
    text_norm = LongTensor(text_norm)
    return text_norm

# def print_speakers(speakers, escape=False):
#     # print('ID\tSpeaker')
#     for id, name in enumerate(speakers):
#         a = f"{id}: {name}"
#         J_speakers['speakers'].append(a)
#         # Save the chat history to a JSON file
#         with open(os.path.join(current_path, "speakers.json"), "w", encoding='utf-8') as outfile:
#             json.dump(J_speakers, outfile, ensure_ascii=False, indent=2)
#         # ex_print(str(id) + '\t' + name, escape)

def get_speaker_id(speaker_id):
    try:
        speaker_id = int(speaker_id)
    except:
        print(str(speaker_id) + ' is not a valid ID!')
        sys.exit(1)
    return speaker_id


def ask_if_continue():
    while True:
        answer = input('Continue? (y/n): ')
        if answer == 'y':
            break
        elif answer == 'n':
            sys.exit(0)

# open model info
with open(model_info, "r", encoding='utf-8') as f:
    f.seek(0)  # Move to the beginning of the file
    model_info = json.loads(f.read())


hps_ms = utils.get_hparams_from_file(model_config)
n_speakers = hps_ms.data.n_speakers if 'n_speakers' in hps_ms.data.keys() else 0
n_symbols = len(hps_ms.symbols) if 'symbols' in hps_ms.keys() else 0
speakers = hps_ms.speakers if 'speakers' in hps_ms.keys() else ['0']
use_f0 = hps_ms.data.use_f0 if 'use_f0' in hps_ms.data.keys() else False
emotion_embedding = hps_ms.data.emotion_embedding if 'emotion_embedding' in hps_ms.data.keys() else False

net_g_ms = SynthesizerTrn(
    n_symbols,
    hps_ms.data.filter_length // 2 + 1,
    hps_ms.train.segment_size // hps_ms.data.hop_length,
    n_speakers=n_speakers,
    emotion_embedding=emotion_embedding,
    **hps_ms.model)
_ = net_g_ms.eval()
utils.load_checkpoint(model, net_g_ms)

escape = False

def synthesize(text: str, speed: float, out_path: str, speaker_id: int):
    if n_symbols != 0:
        if not emotion_embedding:
            # length_scale, text = get_label_value(
            #     text, 'LENGTH', 1.0, 'length scale')
            # noise_scale, text = get_label_value(
            #     text, 'NOISE', 0.667, 'noise scale')
            # noise_scale_w, text = get_label_value(
            #     text, 'NOISEW', 0.8, 'deviation of noise')
            cleaned, text = get_label(text, 'CLEANED')

            stn_tst = get_text(text, hps_ms, cleaned=cleaned)

            # print_speakers(speakers, escape) # print and save speakers.json
            speaker_id = get_speaker_id(speaker_id)
            with no_grad():
                x_tst = stn_tst.unsqueeze(0)
                x_tst_lengths = LongTensor([stn_tst.size(0)])
                sid = LongTensor([speaker_id])
                audio = net_g_ms.infer(x_tst, x_tst_lengths, sid=sid, noise_scale=.667,
                                        noise_scale_w=.8, length_scale=1.0 / speed)[0][0, 0].data.cpu().float().numpy()
      
            write(out_path, hps_ms.data.sampling_rate, audio)