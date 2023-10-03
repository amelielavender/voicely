import discord

from discord import FFmpegPCMAudio
from discord.ext import commands

import os
import sqlite3
import asyncio

from dotenv import load_dotenv
from os import getenv

load_dotenv()

token = getenv("TOKEN")
    
from TTS.api import TTS 

intents = discord.Intents.default() # discord's permission integer
intents.message_content = True # permission scope
intents.members = True # don't know if i need this permission yet

client = discord.Client(intents=intents)

for filename in os.listdir('./cogs'): # read cogs folder
    if filename.endswith('.py'):
        voicely.load_extension(f'cogs.{filename[:-3]}')


voicely = commands.Bot(
        command_prefix = ':',
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


async def join(ctx): # joins vc if msg author is in vc. 
    author = ctx.message.author # get msg author
    voice_chan = ctx.author.voice # join same vs msg author is in
   
    if (voice_chan) and not (ctx.voice_client): # if user in VC and bot not in VC, join same VC
        channel = ctx.message.author.voice.channel
        await channel.connect()
    elif (voice_chan) and (ctx.voice_client): # if already in VC, move on
        pass
    else:
        await ctx.send('You are not in a voice channel.')
        return False


@voicely.command()
async def leave(ctx):
    if (ctx.voice_client):
        await ctx.voice_client.disconnect() 
        await ctx.send('I have left the voice channel')
    else:
        await ctx.send('I am not in a voice channel')

queue = []

@voicely.command()
async def tts(ctx, *, arg):
    if (await join(ctx) == False):
        return

    user = ctx.message.author.display_name 

    # concatenate name and msg received as arg
    message = '{} said: {}'.format(user, arg) 
    if len(queue) > 3:
        await ctx.send('Cannot have more than 3 messages in the queue. Please wait a moment and try again later.')
        return        
    else:
        queue.append(message)

    while not ctx.voice_client.is_playing():
        next(ctx)


def next(ctx):
    if len(queue) != 0:
        tts = TTS(model_name="tts_models/en/ljspeech/glow-tts")
        tts.tts_to_file(text=queue.pop(0), file_path='output.wav') 
        player = ctx.voice_client.play(FFmpegPCMAudio('output.wav'), after=lambda e: next(ctx))


@voicely.command()
async def stop(ctx):
    if ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        if len(queue) < 1:
            await ctx.send('Stopping')
        else:
            await ctx.send('Skipping current message and playing next one.')


# DEBUG
@voicely.command()
async def addq(ctx, *, arg):
    message = arg
    queue.append(message)
    await ctx.send("message has been added to the queue")
    await ctx.send(queue)

@voicely.command()
async def clearq(ctx):
    queue[:] = []
    await ctx.send("queue has been cleared")
   

@voicely.command()
async def hold(ctx):
    await ctx.send('*is hold* 😳')


@voicely.command()
async def ping(ctx):
    await ctx.send('pong')


@voicely.command()
async def get_id(ctx, member: discord.Member):
    id = member.id
    try:
        await ctx.send(f'{member}: {id}')
        await ctx.send(ctx.message.author.id)
    except:
        ctx.send('missing argument')


@voicely.command()
async def db(ctx):
    rows = cursor.execute("SELECT * FROM prefs").fetchall()
    print(rows)

# TODO: guild only commands
# TODO: exit voice call after a while?
# TODO: user prefs via db


voicely.run(token)
