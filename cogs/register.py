# -*- coding: utf-8 -*-

import discord
from discord.ext import commands
from discord import app_commands

from services.skin_analyzer import generate_hash, calculate_similarity
from services.skin_repository import fetch_all_hashes, insert_skin
from storage.r2_storage import upload_image, get_public_url

sessions = {}

# ---------- BOTÃO CANCELAR ----------
class CancelView(discord.ui.View):
    def __init__(self, author_id: int):
        super().__init__(timeout=600)
        self.author_id = author_id

    @discord.ui.button(label="❌ Cancelar", style=discord.ButtonStyle.danger)
    async def cancel(self, interaction: discord.Interaction, _):
        if interaction.user.id != self.author_id:
            await interaction.response.send_message(
                "❌ Só quem iniciou pode cancelar.",
                ephemeral=True
            )
            return

        sessions.pop(self.author_id, None)
        await interaction.response.send_message(
            "❌ Cadastro cancelado.",
            ephemeral=True
        )
        self.stop()


class Register(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ---------- SLASH COMMAND ----------
    @app_commands.command(name="register", description="Cadastrar uma skin")
    async def register(self, interaction: discord.Interaction):
        uid = interaction.user.id

        if uid in sessions:
            await interaction.response.send_message(
                "⚠️ Você já tem um cadastro em andamento.",
                ephemeral=True
            )
            return

        sessions[uid] = {"step": 1}

        await interaction.response.send_message(
            embed=discord.Embed(
                title="📤 Cadastro de Skin",
                description="**Etapa 1**\nEnvie a skin em **PNG**.",
                color=0x5865F2
            ),
            view=CancelView(uid)
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

        # ====== ETAPA 1 — IMAGEM ======
        if session["step"] == 1:
            if not message.attachments:
                return

            attachment = message.attachments[0]
            if not attachment.filename.lower().endswith(".png"):
                await message.channel.send("⚠️ Apenas imagens **PNG** são aceitas.")
                return

            image_bytes = await attachment.read()
            image_hash = generate_hash(image_bytes)

            similar = False
            similarity_value = 0

            # 🔥 CORREÇÃO CRÍTICA: await no banco
            hashes = await fetch_all_hashes()

            for db_hash in hashes:
                similarity = calculate_similarity(image_hash, db_hash)
                if similarity >= 85:
                    similar = True
                    similarity_value = similarity
                    break

            session.update({
                "image_bytes": image_bytes,
                "image_hash": image_hash,
                "step": 2
            })

            if similar:
                await message.channel.send(
                    f"⚠️ **Skin parecida detectada** ({similarity_value:.1f}%). "
                    "Você pode continuar o cadastro."
                )

            await message.channel.send(
                "🆔 **Etapa 2**\nEnvie o **ID do jogador**:",
                view=CancelView(uid)
            )

        # ====== ETAPA 2 — ID DO JOGADOR ======
        elif session["step"] == 2:
            session["user_id"] = message.content.strip()
            session["step"] = 3

            await message.channel.send(
                "🎭 **Etapa 3**\nInforme o **nome do personagem**:",
                view=CancelView(uid)
            )

        # ====== ETAPA 3 — NOME ======
        elif session["step"] == 3:
            session["character_name"] = message.content.strip()
            session["step"] = 4

            await message.channel.send(
                "🧬 **Etapa 4**\nInforme a **raça do personagem**:",
                view=CancelView(uid)
            )

        # ====== ETAPA 4 — FINALIZA ======
        elif session["step"] == 4:
            session["raca"] = message.content.strip()

            # Upload para R2 (sync, ok)
            key = upload_image(
                session["image_bytes"],
                "skin.png"
            )

            # 🔥 CORREÇÃO CRÍTICA: await no insert
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
                    title="✅ Cadastro concluído",
                    description="Skin registrada com sucesso!",
                    color=0x57F287
                )
            )


async def setup(bot):
    await bot.add_cog(Register(bot))
