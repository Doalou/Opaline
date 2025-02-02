# main.py
import discord
from discord.ext import commands
import asyncio
from dotenv import load_dotenv
import os

# Charger les variables d'environnement
load_dotenv()
TOKEN = os.getenv("TOKEN")
APPLICATION_ID = os.getenv("APPLICATION_ID")

if not TOKEN or not APPLICATION_ID:
    raise ValueError("TOKEN ou APPLICATION_ID manquant dans le fichier .env")

# Configuration du bot
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!",
            intents=intents,
            application_id=APPLICATION_ID
        )

    async def setup_hook(self):
        # Chargement des extensions
        for extension in ["cogs.fun", "cogs.moderation", "cogs.utility"]:
            await self.load_extension(extension)
            print(f"Extension {extension} chargée.")
        
        # Synchronisation des commandes
        await self.tree.sync()
        print("Commandes synchronisées avec Discord")

    async def on_ready(self):
        print(f"Bot connecté en tant que {self.user} (Opaline)")

async def main():
    async with Bot() as bot:
        await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())