"""
Real-time audio pipeline for testing the audio engine.

This module routes microphone audio directly to the speaker
to test the real-time audio capture and playback capabilities.
"""

import asyncio

from app.audio.capture import capture_audio
from app.audio.playback import playback_audio


async def main():
    """Run the real-time audio pipeline."""

    print("Audio pipeline started...")

    audio_queue = asyncio.Queue(maxsize=50)

    await asyncio.gather(
        capture_audio(audio_queue),
        playback_audio(audio_queue)
    )


if __name__ == "__main__":
    asyncio.run(main())