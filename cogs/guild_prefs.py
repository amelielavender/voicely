import discord
from discord import app_commands
from discord.ext import commands

import sqlite3 

class settings(commands.Cog):
    def __init__(self, voicely):
        self.voicely = voicely
        self.settings = {}
    
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        connection = sqlite3.connect('preferences.db')
        cursor = connection.cursor()
        id = guild.id
        params = (id, 1)
        cursor.execute('INSERT OR IGNORE INTO guilds (guild_id, x_said) VALUES (?, ?)', params) 
        connection.commit()
        connection.close()

    @commands.command()
    async def set(self, ctx, channel: discord.TextChannel):
        connection = sqlite3.connect('preferences.db')
        cursor = connection.cursor()
        
        id = ctx.guild.id
        tc = channel.id

        cursor.execute('UPDATE guilds SET text_channel_id= ? WHERE guild_id= ? ', (tc, id))
        
        connection.commit()
        connection.close()

    @commands.command()
    async def xsaid(self, ctx, setting):
        connection = sqlite3.connect('preferences.db')
        cursor = connection.cursor()
        
        id = ctx.guild.id

        if setting == 'true':
            cursor.execute('UPDATE guilds SET x_said=1 WHERE guild_id= ? ', [id])
        if setting == 'false':
            cursor.execute('UPDATE guilds SET x_said=0 WHERE guild_id= ? ', [id])

        connection.commit()
        connection.close()
        

async def setup(client):
    await client.add_cog(settings(client))
