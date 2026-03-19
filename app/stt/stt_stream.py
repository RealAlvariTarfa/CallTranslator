import asyncio
import numpy as np
from faster_whisper import WhisperModel

SAMPLE_RATE = 16000
BUFFER_SECONDS = 1


async def streaming_stt(audio_queue: asyncio.Queue, text_queue: asyncio.Queue):

    print("STT task started")

    # ✅ Load model ONLY ONCE
    print("Loading Whisper model...")
    model = WhisperModel(
        "base",
        device="cpu",
        compute_type="int8"
    )
    print("Whisper model loaded.")

    audio_buffer = np.array([], dtype=np.float32)

    while True:
        audio_chunk = await audio_queue.get()

        # ✅ Already float32 → DON'T convert wrongly
        chunk_array = audio_chunk.flatten()

        audio_buffer = np.concatenate((audio_buffer, chunk_array))

        if len(audio_buffer) >= SAMPLE_RATE * BUFFER_SECONDS:

            segments, _ = model.transcribe(
                audio_buffer,
                language="en",
                vad_filter=True
            )

            for segment in segments:
                text = segment.text.strip()
                if text:
                    print(f"You said: {text}")
                    await text_queue.put(text)

            # reset buffer
            audio_buffer = np.array([], dtype=np.float32)