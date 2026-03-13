"""
Real-time pipeline connecting capture, speech recognition, and playback.
"""

import asyncio

from app.audio.capture import capture_audio
from app.audio.playback import playback_audio
from app.stt.stt_stream import streaming_stt


async def main():
    """Run the full real-time pipeline."""

    print("Audio pipeline started...")

    audio_queue = asyncio.Queue(maxsize=50)
    text_queue = asyncio.Queue()

    await asyncio.gather(
        capture_audio(audio_queue),
        streaming_stt(audio_queue, text_queue),
        playback_audio(audio_queue)
    )


if __name__ == "__main__":
    asyncio.run(main())