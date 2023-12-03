import asyncio
import edge_tts

async def TTS(text, voice, rate, volume, pitch, output_file):
    """Main function"""
    communicate = edge_tts.Communicate(text, voice, rate=rate, volume=volume, pitch=pitch)
    await communicate.save(output_file)

def run_tts(text, voice, rate, volume, pitch, output_file):
    print(f"Text: {text}\nVoice: {voice}\npitch: {pitch}\nrate: {rate}\nvolume: {volume}\noutput_file: {output_file}")  
    asyncio.run(TTS(text, voice, rate, volume, pitch, output_file))