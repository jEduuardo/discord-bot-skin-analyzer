import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Carrega variáveis do .env (local)
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

CHANNEL_ID = 1216399451300823050  # ⬅️ ID do canal onde Demeter vai falar


@bot.event
async def on_ready():
    print(f"✅ Bot online como {bot.user}")

    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await channel.send("🌿 **A floresta se renova.**")


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
