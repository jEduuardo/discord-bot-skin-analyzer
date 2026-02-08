import os
import asyncio
import asyncpg
from dotenv import load_dotenv

load_dotenv()  # 👈 carrega o .env

async def main():
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise RuntimeError("DATABASE_URL não foi encontrada no .env")

    conn = await asyncpg.connect(database_url)
    print("✅ Conectado com sucesso ao Neon!")
    await conn.close()

asyncio.run(main())
