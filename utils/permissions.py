import discord

CREATOR_ID = 500033555020382244
ALLOWED_CHANNEL_ID = 1216399451300823050  # <-- troque pelo ID real


async def can_execute(interaction: discord.Interaction) -> bool:
    # Criador pode tudo
    # if interaction.user.id == CREATOR_ID:
    #     return True

    # Admin pode tudo
    # if interaction.user.guild_permissions.administrator:
    #     return True

    # Canal permitido
    if interaction.channel_id == ALLOWED_CHANNEL_ID:
        return True

    # Bloqueado
    await interaction.response.send_message(
        "🍀 **Opa! Minhas vinhas não alcançam este jardim...**\n"
        "Para me invocar, siga até 🌳 <#{}> 🌻🌱".format(ALLOWED_CHANNEL_ID),
        ephemeral=False
    )
    return False
