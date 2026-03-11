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


async def capture_audio(queue: asyncio.Queue) -> None:
    """
    Capture audio from microphone and push chunks to asyncio queue.
    
    This function starts a non-blocking InputStream using sounddevice's
    callback mechanism, ensuring the asyncio event loop is not blocked.
    Audio is converted to PCM16 format before being put into the queue.
    
    Args:
        queue: An asyncio.Queue to push audio chunks into.
              Each chunk is a bytes object containing PCM16 audio data.
    
    Returns:
        None - runs indefinitely until stopped.
    """
    loop = asyncio.get_running_loop()
    stream_started = asyncio.Event()
    
    def callback(indata: np.ndarray, frames: int, time_info, status: sd.CallbackFlags) -> None:
        """
        Sounddevice callback function called for each audio chunk.
        
        This callback runs in a separate thread, so we use loop.call_soon_threadsafe
        to safely put data into the asyncio queue.
        """
        if status:
            print(f"Audio capture status: {status}")
        
        # Convert to PCM16 format (int16)
        # indata shape: (frames, channels), dtype: float32
        # Scale from [-1.0, 1.0] to int16 range
        audio_int16 = (indata.flatten() * 32767).astype(np.int16)
        
        # Convert to bytes (PCM16)
        audio_bytes = audio_int16.tobytes()
        
        # Put the audio chunk into the queue (thread-safe)
        def safe_put():
            if not queue.full():
                queue.put_nowait(audio_bytes)

        loop.call_soon_threadsafe(safe_put)
    
    # Create the input stream with the callback
    with sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype=np.float32,
        blocksize=CHUNK_SAMPLES,
        latency="low",
        callback=callback
    ):
        # Keep the stream running - this is a blocking context manager
        # The stream runs in a separate thread and uses callbacks
        # We use a future to keep this coroutine alive
        await asyncio.sleep(float('inf'))

