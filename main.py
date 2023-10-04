import discord

from discord.ext import commands

import os
import sqlite3
import asyncio

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

connection = sqlite3.connect('preferences.db')
cursor = connection.cursor()
# returns a cursor object that lets us use sql statements using cursor.execute()

@voicely.event
async def on_ready():
    print(f'logging on as {voicely.user}')
    #cursor.execute('INSERT OR IGNORE()')
    

@voicely.command()
async def set(ctx, language, voice):
    try:
        id = ctx.message.author.id 
        params = (id, language, voice)
        cursor.execute('INSERT INTO prefs VALUES (?, ?, ?)',params)
    except:
        await ctx.send('u scrunbled it')

# DEBUG
@voicely.command()
async def clearq(ctx):
    queue[:] = []
    await ctx.send("queue has been cleared")
   

@voicely.command()   
async def addq(ctx, *, arg):
    queue.append(arg)
    await ctx.send('message has been addeed to `queue[]`')
    await ctx.send(queue)

# TODO: guild only commands
# TODO: exit voice call after a while?
# TODO: user prefs via db

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


async def main():
    # TODO: try/except to handle cleanup on KeyboardInterrupt()
    async with voicely:
        await load_ext() 
        
asyncio.run(main())

voicely.run(token)

