# -*- coding: utf-8 -*-
import discord
from discord.ext import commands
from utils.permissions import can_execute


class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(
        name="ping",
        description="Mostra a latência do bot"
    )
    async def ping(self, interaction: discord.Interaction):

        if not await can_execute(interaction):
            return

        latency_ms = round(self.bot.latency * 1000)

        await interaction.response.send_message(
            f"🏓 Pong!\n📡 Latência: **{latency_ms} ms**"
        )


async def setup(bot):
    await bot.add_cog(Ping(bot))
