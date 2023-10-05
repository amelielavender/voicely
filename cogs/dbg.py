import discord
from discord.ext import commands

class debug(commands.Cog):
    def __init__(self, voicely):
        self.voicely = voicely


    @commands.command()
    async def db(self, ctx):
        rows = cursor.execute("SELECT * FROM prefs").fetchall()
        print(rows) 


    @commands.command()
    async def ping(self, ctx):
        await ctx.send('pong')


    @commands.command()
    async def get_id(self, ctx, member: discord.Member):
        id = member.id
        try:
            await ctx.send(f'{member}: {id}')
        except:
            await ctx.send('usage: :get_id `@user`')


async def setup(client):
    await client.add_cog(debug(client))
