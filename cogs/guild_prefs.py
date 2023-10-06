import discord
from discord import app_commands
from discord.ext import commands
import sqlite3 

class settings(commands.Cog):
    def __init__(self, voicely):
        self.voicely = voicely
    
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        connection = sqlite3.connect('preferences.db')
        cursor = connection.cursor()
        id = guild.id
        params = (id, 1)
        cursor.execute('INSERT OR IGNORE INTO guilds (guild_id, x_said) VALUES (?, ?)', params) 
        connection.commit()
        connection.close()

    @commands.hybrid_command(name='set', description='sets the text channel that voicely will listen to')
    async def set(self, ctx: commands.Context, channel: discord.TextChannel) -> None:
        connection = sqlite3.connect('preferences.db')
        cursor = connection.cursor()
        
        id = ctx.guild.id
        tc = channel.id

        cursor.execute('UPDATE guilds SET text_channel_id= ? WHERE guild_id= ? ', (tc, id))
        
        connection.commit()
        connection.close()
        await ctx.send(f'now watching {channel} :eyes:')

    @commands.hybrid_command(name='xsaid', description='enables/disables x said prefix when speaking')
    async def xsaid(self, ctx: commands.Context, setting: str) -> None:
        connection = sqlite3.connect('preferences.db')
        cursor = connection.cursor()
        
        id = ctx.guild.id

        if setting == 'true':
            cursor.execute('UPDATE guilds SET x_said=1 WHERE guild_id= ? ', [id])
        if setting == 'false':
            cursor.execute('UPDATE guilds SET x_said=0 WHERE guild_id= ? ', [id])

        connection.commit()
        connection.close()
        await ctx.send(f'x said setting is now: {setting}')
        

async def setup(client):
    await client.add_cog(settings(client))
