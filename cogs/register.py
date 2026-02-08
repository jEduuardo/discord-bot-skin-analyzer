# -*- coding: utf-8 -*-

import discord
from discord.ext import commands
from discord import app_commands

from services.skin_analyzer import generate_hash, calculate_similarity
from services.skin_repository import fetch_all_hashes, insert_skin
from storage.r2_storage import upload_image, get_public_url

sessions = {}

# ---------- VIEW CONFIRMAR ----------
class ConfirmView(discord.ui.View):
    def __init__(self, uid: int):
        super().__init__(timeout=300)
        self.uid = uid
        self.value = None

    @discord.ui.button(label="✅ Continuar", style=discord.ButtonStyle.success)
    async def confirm(self, interaction: discord.Interaction, _):
        if interaction.user.id != self.uid:
            return await interaction.response.send_message(
                "❌ Apenas quem iniciou pode responder.",
                ephemeral=True
            )

        self.value = True
        self.stop()
        await interaction.response.defer()

    @discord.ui.button(label="❌ Cancelar", style=discord.ButtonStyle.danger)
    async def cancel(self, interaction: discord.Interaction, _):
        sessions.pop(self.uid, None)
        self.value = False
        self.stop()
        await interaction.response.send_message(
            "❌ Cadastro cancelado.",
            ephemeral=True
        )


class Register(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ---------- SLASH ----------
    @app_commands.command(name="register", description="Cadastrar uma skin")
    async def register(self, interaction: discord.Interaction):
        uid = interaction.user.id

        if uid in sessions:
            return await interaction.response.send_message(
                "⚠️ Você já tem um cadastro em andamento.",
                ephemeral=True
            )

        sessions[uid] = {"step": 1}

        await interaction.response.send_message(
            embed=discord.Embed(
                title="📤 Cadastro de Skin",
                description="**Etapa 1**\nEnvie a skin em **PNG**.",
                color=0x5865F2
            )
        )

    # ---------- LISTENER ----------
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        uid = message.author.id
        if uid not in sessions:
            return

        session = sessions[uid]

        # ===== ETAPA 1 — SKIN =====
        if session["step"] == 1:
            if not message.attachments:
                return

            att = message.attachments[0]
            if not att.filename.lower().endswith(".png"):
                return await message.channel.send("⚠️ Apenas **PNG**.")

            log_msg = await message.channel.send(
                "🧪 **Gerando hash da skin...**"
            )

            image_bytes = await att.read()
            image_hash = generate_hash(image_bytes)

            await log_msg.edit(
                content=(
                    "🧪 **Gerando hash da skin...**\n"
                    f"✅ Hash gerado: `{image_hash}`\n\n"
                    "🔍 **Verificando semelhança no banco de dados...**"
                )
            )

            hashes = await fetch_all_hashes()

            similar = False
            similarity_value = 0

            for db_hash in hashes:
                similarity = calculate_similarity(image_hash, db_hash)
                if similarity >= 85:
                    similar = True
                    similarity_value = similarity
                    break

            session["image_bytes"] = image_bytes
            session["image_hash"] = image_hash

            if similar:
                view = ConfirmView(uid)
                await log_msg.edit(
                    content=(
                        f"⚠️ **Skin semelhante detectada**\n"
                        f"Similaridade: **{similarity_value:.1f}%**\n\n"
                        "Deseja continuar?"
                    ),
                    view=view
                )

                await view.wait()
                if not view.value:
                    return

            else:
                await log_msg.edit(
                    content=(
                        "🔍 **Verificando semelhança no banco de dados...**\n"
                        "✅ Nenhuma semelhança encontrada."
                    )
                )

            session["step"] = 2
            await message.channel.send("🆔 **Etapa 2**\nInforme o **ID do jogador**:")

        # ===== ETAPA 2 =====
        elif session["step"] == 2:
            session["user_id"] = message.content.strip()
            session["step"] = 3
            await message.channel.send("🎭 **Etapa 3**\nNome do personagem:")

        # ===== ETAPA 3 =====
        elif session["step"] == 3:
            session["character_name"] = message.content.strip()
            session["step"] = 4
            await message.channel.send("🧬 **Etapa 4**\nRaça do personagem:")

        # ===== ETAPA 4 — FINAL =====
        elif session["step"] == 4:
            session["raca"] = message.content.strip()

            key = upload_image(session["image_bytes"], "skin.png")

            await insert_skin(
                user_id=session["user_id"],
                character_name=session["character_name"],
                raca=session["raca"],
                image_url=get_public_url(key),
                image_hash=session["image_hash"],
                created_by=uid
            )

            sessions.pop(uid, None)

            await message.channel.send(
                embed=discord.Embed(
                    title="🌱 Cadastro concluído",
                    description="A semente foi plantada. A floresta se renova.",
                    color=0x57F287
                )
            )


async def setup(bot):
    await bot.add_cog(Register(bot))
