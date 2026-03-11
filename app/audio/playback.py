import asyncio
import sounddevice as sd
import numpy as np
import queue as thread_queue

SAMPLE_RATE = 16000
CHANNELS = 1
CHUNK_DURATION_MS = 20
CHUNK_SAMPLES = int(SAMPLE_RATE * CHUNK_DURATION_MS / 1000)


async def playback_audio(queue: asyncio.Queue):

    loop = asyncio.get_running_loop()

    # Thread-safe queue used by audio callback
    audio_buffer = thread_queue.Queue(maxsize=50)

    # Transfer data from asyncio queue → thread queue
    async def queue_worker():
        while True:
            chunk = await queue.get()
            try:
                audio_buffer.put_nowait(chunk)
            except thread_queue.Full:
                pass

    def callback(outdata, frames, time_info, status):

        if status:
            print(status)

        try:
            audio_bytes = audio_buffer.get_nowait()
            audio = np.frombuffer(audio_bytes, dtype=np.int16)
        except thread_queue.Empty:
            audio = np.zeros(frames, dtype=np.int16)

        if len(audio) < frames:
            padded = np.zeros(frames, dtype=np.int16)
            padded[:len(audio)] = audio
            audio = padded

        outdata[:] = audio.reshape(-1, 1)

    with sd.OutputStream(
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype=np.int16,
        blocksize=CHUNK_SAMPLES,
        latency="low",
        callback=callback,
    ):

        await queue_worker()