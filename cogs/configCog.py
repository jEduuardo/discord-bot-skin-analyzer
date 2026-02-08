# -*- coding: utf-8 -*-
import discord
from discord.ext import commands

class ConfigCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("?? ConfigCog carregado com sucesso")


async def setup(bot):
    await bot.add_cog(ConfigCog(bot))
