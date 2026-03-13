import asyncio


async def test1():
    print("Task 1 started")
    while True:
        await asyncio.sleep(1)


async def test2():
    print("Task 2 started")
    while True:
        await asyncio.sleep(1)


async def main():

    print("Audio pipeline started...")

    await asyncio.gather(
        test1(),
        test2(),
    )