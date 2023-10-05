import discord
from discord import app_commands
from discord.ext import commands

class Gprefs(commands.Cog):
    def __init__(self, voicely):
        self.voicely = voicely

    
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        id = guild.id
        print(id)
        
async def setup(client):
    await client.add_cog(Gprefs(client))
