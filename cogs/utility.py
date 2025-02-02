# cogs/utility.py
import discord
from discord import app_commands
from discord.ext import commands

class Utility(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="info", description="Affiche des informations sur le bot")
    async def info(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Opaline",
            description="Bot multifonctions en Python utilisant discord.py et les slash commandes.",
            color=discord.Color.blue()
        )
        embed.add_field(name="Créateur", value="Doalo", inline=True)
        embed.add_field(name="Langage", value="Python", inline=True)
        embed.set_footer(text="Opaline - Bot créé par Doalo")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="userinfo", description="Affiche des informations sur un utilisateur")
    async def userinfo(self, interaction: discord.Interaction, member: discord.Member = None):
        member = member or interaction.user
        embed = discord.Embed(
            title=f"Informations sur {member}",
            color=discord.Color.purple()
        )
        embed.add_field(name="Nom", value=member.name, inline=True)
        embed.add_field(name="ID", value=member.id, inline=True)
        embed.add_field(name="Compte créé le", value=member.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
        if member.avatar:
            embed.set_thumbnail(url=member.avatar.url)
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Utility(bot))