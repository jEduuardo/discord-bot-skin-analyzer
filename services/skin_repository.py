# -*- coding: utf-8 -*-
import os
import asyncpg
from typing import List

DATABASE_URL = os.getenv("DATABASE_URL")

_pool: asyncpg.pool.Pool | None = None

# ---------- RESET POOL ----------
async def reset_pool():
    """Fecha o pool atual (se existir) e força criação de um novo."""
    global _pool
    if _pool is not None:
        await _pool.close()
    _pool = None

# ---------- GET POOL ----------
async def get_pool() -> asyncpg.pool.Pool:
    """Retorna o pool de conexões, criando se necessário."""
    global _pool
    if _pool is None:
        _pool = await asyncpg.create_pool(
            DATABASE_URL,
            statement_cache_size=0  # ⚠️ evita erros de cache de prepared statements
        )
    return _pool

# ---------- FETCH HASHES ----------
async def fetch_all_hashes() -> List[str]:
    """Retorna todos os image_hash do banco."""
    pool = await get_pool()
    async with pool.acquire() as conn:
        try:
            rows = await conn.fetch("SELECT image_hash FROM skins")
        except asyncpg.exceptions.InvalidCachedStatementError:
            # Caso o cache esteja inválido, recarrega schema e tenta de novo
            await conn.reload_schema_state()
            rows = await conn.fetch("SELECT image_hash FROM skins")
        return [row["image_hash"] for row in rows]

# ---------- INSERT SKIN ----------
async def insert_skin(
    user_id: int,
    character_name: str,
    raca: str,
    image_url: str,
    image_hash: str,
    created_by: int
):
    """Insere uma skin no banco de dados."""
    pool = await get_pool()
    async with pool.acquire() as conn:
        async with conn.transaction():
            try:
                await conn.execute(
                    """
                    INSERT INTO skins (
                        user_id,
                        character_name,
                        raca,
                        image_url,
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
            except asyncpg.exceptions.InvalidCachedStatementError:
                # Caso ocorra erro de cache, recarrega schema e tenta novamente
                await conn.reload_schema_state()
                await conn.execute(
                    """
                    INSERT INTO skins (
                        user_id,
                        character_name,
                        raca,
                        image_url,
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
