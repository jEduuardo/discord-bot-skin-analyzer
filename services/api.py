import aiohttp
from config import API_BASE_URL

async def analyze_skin(image_bytes: bytes):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{API_BASE_URL}/analyze-skin",
            data=image_bytes
        ) as resp:
            return await resp.json()


async def finalize_register(payload: dict):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{API_BASE_URL}/finalize-register",
            json=payload
        ) as resp:
            return await resp.json()
