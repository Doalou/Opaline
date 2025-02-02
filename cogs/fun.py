# cogs/fun.py
import discord
from discord import app_commands
from discord.ext import commands
import random

class Fun(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="ping", description="Le bot répond 'Pong!'")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message("Pong!")

    @app_commands.command(name="roll", description="Lance un dé avec un nombre de faces spécifié (par défaut 6)")
    async def roll(self, interaction: discord.Interaction, sides: int = 6):
        result = random.randint(1, sides)
        await interaction.response.send_message(f"🎲 Dé à {sides} faces : {result}")

    @app_commands.command(name="say", description="Fait répéter un message par le bot")
    async def say(self, interaction: discord.Interaction, message: str):
        await interaction.response.send_message(message)

    @app_commands.command(name="choose", description="Choisit aléatoirement parmi plusieurs options (séparées par des virgules)")
    async def choose(self, interaction: discord.Interaction, options: str):
        opts = [option.strip() for option in options.split(",") if option.strip()]
        if not opts:
            await interaction.response.send_message("Aucune option valide fournie.", ephemeral=True)
            return
        choice = random.choice(opts)
        await interaction.response.send_message(f"Je choisis : {choice}")

async def setup(bot: commands.Bot):
    await bot.add_cog(Fun(bot))