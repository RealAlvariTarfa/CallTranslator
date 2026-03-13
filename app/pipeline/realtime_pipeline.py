import asyncio

from app.audio.capture import capture_audio
from app.audio.playback import playback_audio
from app.stt.stt_stream import streaming_stt


async def main():

    print("Audio pipeline started...")

    audio_queue = asyncio.Queue(maxsize=50)
    text_queue = asyncio.Queue()

    loop = asyncio.get_running_loop()

    await asyncio.gather(

        # run capture in background thread
        loop.run_in_executor(None, capture_audio, audio_queue),

        # STT task
        streaming_stt(audio_queue, text_queue),

        # playback task
        playback_audio(audio_queue),
    )