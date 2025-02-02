# cogs/moderation.py
import discord
from discord import app_commands
from discord.ext import commands
from typing import Optional

class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="kick", description="Expulse un membre du serveur")
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = "Aucune raison fournie"):
        # Vérifications de base
        if member == interaction.user:
            await interaction.response.send_message("Vous ne pouvez pas vous expulser vous-même.", ephemeral=True)
            return
            
        if member.top_role >= interaction.user.top_role:
            await interaction.response.send_message("Vous ne pouvez pas expulser ce membre car son rôle est supérieur ou égal au vôtre.", ephemeral=True)
            return
        
        if member.top_role >= interaction.guild.me.top_role:
            await interaction.response.send_message("Je ne peux pas expulser ce membre car son rôle est supérieur au mien.", ephemeral=True)
            return

        try:
            # Création de l'embed
            embed = discord.Embed(
                title="👢 Expulsion",
                description=f"{member.mention} a été expulsé du serveur.",
                color=discord.Color.orange()
            )
            embed.add_field(name="Raison", value=reason)
            embed.add_field(name="Modérateur", value=interaction.user.mention)
            
            # Tentative d'envoi du message privé
            try:
                await member.send(f"Vous avez été expulsé de {interaction.guild.name} pour la raison suivante : {reason}")
            except discord.Forbidden:
                pass  # On continue même si le message privé ne peut pas être envoyé
            
            # Expulsion du membre
            await member.kick(reason=f"Par {interaction.user}: {reason}")
            await interaction.response.send_message(embed=embed)
        
        except discord.Forbidden:
            await interaction.response.send_message("Je n'ai pas les permissions nécessaires pour expulser ce membre.", ephemeral=True)
        except discord.HTTPException:
            await interaction.response.send_message("Une erreur s'est produite lors de l'expulsion.", ephemeral=True)

    @app_commands.command(name="ban", description="Bannit un membre du serveur")
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str = "Aucune raison fournie", delete_messages_days: Optional[int] = 0):
        # Vérifications de base
        if member == interaction.user:
            await interaction.response.send_message("Vous ne pouvez pas vous bannir vous-même.", ephemeral=True)
            return

        if not 0 <= delete_messages_days <= 7:
            await interaction.response.send_message("Le nombre de jours de messages à supprimer doit être entre 0 et 7.", ephemeral=True)
            return

        if member.top_role >= interaction.user.top_role:
            await interaction.response.send_message("Vous ne pouvez pas bannir ce membre car son rôle est supérieur ou égal au vôtre.", ephemeral=True)
            return
        
        if member.top_role >= interaction.guild.me.top_role:
            await interaction.response.send_message("Je ne peux pas bannir ce membre car son rôle est supérieur au mien.", ephemeral=True)
            return

        try:
            # Création de l'embed
            embed = discord.Embed(
                title="🔨 Bannissement",
                description=f"{member.mention} a été banni du serveur.",
                color=discord.Color.red()
            )
            embed.add_field(name="Raison", value=reason)
            embed.add_field(name="Modérateur", value=interaction.user.mention)
            embed.add_field(name="Messages supprimés", value=f"Messages des {delete_messages_days} derniers jours")
            
            # Tentative d'envoi du message privé
            try:
                await member.send(f"Vous avez été banni de {interaction.guild.name} pour la raison suivante : {reason}")
            except discord.Forbidden:
                pass  # On continue même si le message privé ne peut pas être envoyé
            
            # Bannissement du membre
            await member.ban(reason=f"Par {interaction.user}: {reason}", delete_message_days=delete_messages_days)
            await interaction.response.send_message(embed=embed)
        
        except discord.Forbidden:
            await interaction.response.send_message("Je n'ai pas les permissions nécessaires pour bannir ce membre.", ephemeral=True)
        except discord.HTTPException:
            await interaction.response.send_message("Une erreur s'est produite lors du bannissement.", ephemeral=True)

    @app_commands.command(name="clear", description="Supprime un nombre spécifié de messages")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def clear(self, interaction: discord.Interaction, amount: int):
        if amount < 1 or amount > 100:
            await interaction.response.send_message("Le nombre de messages à supprimer doit être compris entre 1 et 100.", ephemeral=True)
            return

        try:
            await interaction.response.defer(ephemeral=True)
            # Ajout de 1 pour inclure le message de commande
            deleted = await interaction.channel.purge(limit=amount + 1)
            # On soustrait 1 pour ne pas compter le message de commande
            await interaction.followup.send(f"✨ {len(deleted) - 1} messages ont été supprimés.", ephemeral=True)
        
        except discord.Forbidden:
            await interaction.followup.send("Je n'ai pas les permissions nécessaires pour supprimer des messages.", ephemeral=True)
        except discord.HTTPException:
            await interaction.followup.send("Une erreur s'est produite lors de la suppression des messages.", ephemeral=True)

    @app_commands.command(name="server", description="Affiche des informations sur le serveur")
    async def server(self, interaction: discord.Interaction):
        guild = interaction.guild
        embed = discord.Embed(
            title=f"ℹ️ Informations sur {guild.name}",
            color=discord.Color.blue()
        )
        embed.add_field(name="ID du serveur", value=guild.id, inline=True)
        embed.add_field(name="Propriétaire", value=guild.owner.mention, inline=True)
        embed.add_field(name="Membres", value=guild.member_count, inline=True)
        embed.add_field(name="Salons", value=len(guild.channels), inline=True)
        embed.add_field(name="Rôles", value=len(guild.roles), inline=True)
        embed.add_field(name="Date de création", value=guild.created_at.strftime("%d/%m/%Y"), inline=True)
        
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Moderation(bot))
