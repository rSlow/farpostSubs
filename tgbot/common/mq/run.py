import asyncio

from common.mq.app import app


async def __main__():
    await app.run()


if __name__ == '__main__':
    asyncio.run(__main__())
