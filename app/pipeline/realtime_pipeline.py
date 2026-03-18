import asyncio

from app.audio.capture import capture_audio
from app.audio.playback import playback_audio
from app.stt.stt_stream import streaming_stt


async def main():

    print("Audio pipeline started...")

    audio_queue = asyncio.Queue(maxsize=100)     # for STT
    playback_queue = asyncio.Queue(maxsize=100)  # for speakers
    text_queue = asyncio.Queue()

    capture_task = asyncio.create_task(
        capture_audio(audio_queue, playback_queue)
    )

    stt_task = asyncio.create_task(
        streaming_stt(audio_queue, text_queue)
    )

    playback_task = asyncio.create_task(
        playback_audio(playback_queue)
    )

    await asyncio.gather(
        capture_task,
        stt_task,
        playback_task,
    )