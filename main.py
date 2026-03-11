"""
Entry point for the real-time audio pipeline.

This module imports and runs the main() function from
app.pipeline.realtime_pipeline using asyncio.run().
"""

import asyncio

from app.pipeline.realtime_pipeline import main


if __name__ == "__main__":
    asyncio.run(main())

