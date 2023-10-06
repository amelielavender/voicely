import discord, asyncio, os

from discord import app_commands
from discord.ext import commands 

from dotenv import load_dotenv
from os import getenv

load_dotenv()

token = getenv("TOKEN")
    
intents = discord.Intents.default() # discord's permission integer
intents.message_content = True # permission scope
intents.members = True # don't know if i need this permission yet


voicely = commands.Bot(
        command_prefix = ';',
        description = 'TODO',
        intents = intents
        )


@voicely.event
async def on_ready():
    print(f'logging on as {voicely.user}')
    await load_ext()


@voicely.command()
@commands.is_owner()
async def sync(ctx):
    await bot.tree.sync()
    await ctx.send('syncing to global namespace')


async def load_ext():
    for filename in os.listdir('./cogs'): # read cogs folder
        if filename.endswith('.py'):
            await voicely.load_extension(f'cogs.{filename[:-3]}')


@voicely.command()
async def load(ctx, mycog):
    await voicely.load_extension(f'cogs.{mycog}')


@voicely.command()
async def unload(ctx, mycog):
    await voicely.unload_extension(f'cogs.{mycog}')


#async def main():
    # TODO: try/except to handle cleanup on KeyboardInterrupt()
    #async with voicely:
        #await load_ext() 
        
#asyncio.start(main())

voicely.run(token)

