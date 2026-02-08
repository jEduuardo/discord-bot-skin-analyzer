# services/skin_repository.py
import os
import asyncpg

DATABASE_URL = os.getenv("DATABASE_URL")

_pool = None


async def get_pool():
    global _pool
    if _pool is None:
        _pool = await asyncpg.create_pool(DATABASE_URL)
    return _pool


async def fetch_all_hashes():
    pool = await get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch("SELECT image_hash FROM skins")
        return [row["image_hash"] for row in rows]


async def insert_skin(
    user_id: int,
    character_name: str,
    raca: str,
    image_url: str,
    image_hash: str,
    created_by: int
):
    pool = await get_pool()
    async with pool.acquire() as conn:
        await conn.execute(
            """
            INSERT INTO skins (
                user_id,
                character_name,
                raca,
                imagem_url,
                image_hash,
                created_at,
                created_by
            )
            VALUES ($1, $2, $3, $4, $5, NOW(), $6)
            """,
            user_id,
            character_name,
            raca,
            image_url,
            image_hash,
            created_by
        )
