from pathlib import Path

import aiofiles


async def save_page(path: Path,
                    data: bytes):
    path.parent.mkdir(parents=True, exist_ok=True)
    async with aiofiles.open(path, "wb") as file:
        await file.write(data)
