import discord 
import asyncio
from discord import app_commands
from discord.ext import commands 
from dotenv import load_dotenv
import os

load_dotenv()

token = os.getenv("TOKEN")
    
intents = discord.Intents.default() # discord's permission integer
intents.message_content = True # permission scope
intents.members = True  


voicely = commands.Bot(
        command_prefix = ';',
        description = 'DESC',
        intents = intents
        )


@voicely.event
async def on_ready():
    print(f'logging on as {voicely.user.id}')
    await load_ext()


@voicely.command()
@commands.is_owner()
async def sync(ctx):
    await voicely.tree.sync(guild=ctx.guild)
    await voicely.tree.sync()
    await ctx.send('syncing to global namespace')


async def load_ext():
    for filename in os.listdir('./cogs'): # read cogs folder
        if filename.endswith('.py'):
            await voicely.load_extension(f'cogs.{filename[:-3]}')


@voicely.command(name='load', hidden=True)
@commands.is_owner()
async def load(ctx, mycog):
    try:
        await voicely.load_extension(f'cogs.{mycog}')
        await ctx.send(f'loaded {mycog}')
    except:
        await ctx.send('something went wrong')

@voicely.command(name='unload', hidden=True)
@commands.is_owner()
async def unload(ctx, mycog):
    try:
        await voicely.unload_extension(f'cogs.{mycog}')
        await ctx.send(f'unloaded {mycog}')
    except:
        await ctx.send('something went wrong')


@voicely.command(name='reload', hidden=True)
@commands.is_owner()
async def rel(ctx, mycog):
    try:
        await voicely.reload_extension(f'cogs.{mycog}')
        await ctx.send(f'reloading {mycog}')
    except:
        await ctx.send('something went wrong')


#async def main():
    # TODO: try/except to handle cleanup on KeyboardInterrupt()
    #async with voicely:
        #await load_ext() 
        
#asyncio.start(main())

voicely.run(token)

