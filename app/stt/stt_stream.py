async def streaming_stt(audio_queue: asyncio.Queue, text_queue: asyncio.Queue):

    print("STT task started")

    print("Loading Whisper model...")

    model = WhisperModel(
        "base",
        device="cpu",
        compute_type="int8"
    )

    print("Whisper model loaded.")
    print("STT engine starting...")

    audio_buffer = []

    while True:
        audio_chunk = await audio_queue.get()

        # ✅ audio_chunk is already float32 from sounddevice
        audio_buffer.append(audio_chunk)

        # accumulate ~1 second
        if len(audio_buffer) < 50:
            continue

        # merge chunks
        audio_np = np.concatenate(audio_buffer, axis=0)

        # flatten to 1D
        audio_np = audio_np.flatten()

        print("Processing audio...")

        segments, _ = model.transcribe(
            audio_np,
            language="en",
            vad_filter=True
        )

        for segment in segments:
            text = segment.text.strip()

            if text:
                print(f"You said: {text}")
                await text_queue.put(text)

        # reset buffer
        audio_buffer = []