import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Carrega variáveis do .env (local)
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
<<<<<<< HEAD
intents.message_content = True

=======
>>>>>>> fba511dfb6b5229b5842777eae7386494812dd68

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

@bot.event
async def on_ready():
    print(f"✅ Bot online como {bot.user}")

# 🔌 Carregar todos os cogs automaticamente
async def load_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")
            print(f"📦 Cog carregado: {filename}")

@bot.event
async def setup_hook():
    await load_cogs()
    try:
        synced = await bot.tree.sync()
        print(f"🔁 Slash commands sincronizados: {len(synced)}")
    except Exception as e:
        print(f"Erro ao sincronizar comandos: {e}")

bot.run(TOKEN)
