print("STT module imported")
"""
Real-time streaming speech-to-text module using faster-whisper.
"""

import asyncio
import numpy as np
from faster_whisper import WhisperModel

print("STT module loaded")

SAMPLE_RATE = 16000
BUFFER_SECONDS = 1


async def streaming_stt(audio_queue: asyncio.Queue, text_queue: asyncio.Queue):

    print("STT task started")

    print("Loading Whisper model...")

    model = WhisperModel("base", compute_type="int8")

    print("Whisper model loaded")


    print("STT engine starting...")
    """
    Continuously read audio chunks from the audio_queue and perform speech recognition.
    Recognized text is pushed to text_queue.
    """

    print("Loading Whisper model...")

    model = WhisperModel(
        "base",
        device="cpu",
        compute_type="int8"
    )

    print("Whisper model loaded.")

    audio_buffer = np.array([], dtype=np.int16)

    while True:

        audio_chunk = await audio_queue.get()

        chunk_array = np.frombuffer(audio_chunk, dtype=np.int16)

        audio_buffer = np.concatenate((audio_buffer, chunk_array))

        if len(audio_buffer) >= SAMPLE_RATE * BUFFER_SECONDS:

            audio_float = audio_buffer.astype(np.float32) / 32768.0

            segments, _ = model.transcribe(
                audio_float,
                language="en",
                vad_filter=True
            )

            for segment in segments:

                text = segment.text.strip()

                if text:
                    print(f"You said: {text}")

                    await text_queue.put(text)

            audio_buffer = np.array([], dtype=np.int16)