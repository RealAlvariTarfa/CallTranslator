"""
Real-time audio capture module using sounddevice.

This module provides async audio capture functionality that streams
PCM16 audio chunks from the microphone into an asyncio queue.
"""

import asyncio
import sounddevice as sd
import numpy as np
from typing import AsyncGenerator

# Audio configuration constants
SAMPLE_RATE = 16000  # 16000 Hz
CHANNELS = 1  # Mono channel
CHUNK_DURATION_MS = 20  # 20 ms chunks
CHUNK_SAMPLES = int(SAMPLE_RATE * CHUNK_DURATION_MS / 1000)  # 320 samples


async def capture_audio(audio_queue):

    print("Microphone capture starting...")

    loop = asyncio.get_running_loop()

    def callback(indata, frames, time, status):
        if status:
            print(status)

        audio = indata.copy()

        try:
            audio_queue.put_nowait(indata.copy())
        except asyncio.QueueFull:
            pass  # drop audio instead of crashing

        # print("Audio chunk captured")

    stream = sd.InputStream(
        samplerate=16000,
        channels=1,
        blocksize=320,   # ✅ 20ms chunks (IMPORTANT)
        dtype="float32",
        callback=callback,
    )

    with stream:
        print("Microphone stream opened")

        while True:
            await asyncio.sleep(1)