from aiohttp import ClientSession


async def download_page(session: ClientSession,
                        url: str):
    await session.get("https://www.farpost.ru/")  # get cookies
    async with session.get(url) as response:
        data = await response.content.read()
    return data
