import discord
from discord import FFmpegPCMAudio
from discord.ext import commands

from typing import Dict

from gtts import gTTS

import sqlite3

class TTSq:
    def __init__(self, id: int): # the only thing we need to pass in is an id variable. we annotate with the colon after the variable name.
        self.id = id
        self.queue = [] # queue variable, type of Queue's max size 

    def add_msg(self, msg):
        self.queue.append(msg)

    @property
    def is_full(self):
        if len(self.queue) > 3:
            return True


""" every TTSq object has a queue of size 3 associated with it
    additionally, it has a method called add_msg. 
    we will initialize a new cog and create a dictionary for the cog.
    the dictionary contains keys that are ints, whose values are the TTSq object we made.
"""

class voice_commands(commands.Cog):
    def __init__(self, voicely):
        self.voicely = voicely
        self.queues: Dict[int, TTSq] = {} 


    async def join(self, ctx): # joins vc if msg author is in vc. 
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


    @commands.command()
    async def tts(self, ctx, *, arg):
        if (await self.join(ctx) == False):
            return
        else:
            await self.speak(ctx, arg)


    async def speak(self, ctx, msg):
        guild = ctx.guild.id
        q = self.queues.get(guild, TTSq(guild)) # get current guild's queue from qs Dict
        self.queues[guild] = q # assign q's value to qs[guild]'s key

        user = ctx.message.author.display_name 

        # concatenate name and msg received as arg
        message = '{} said: {}'.format(user, msg) 

        if q.is_full:
            await ctx.send('Cannot have more than 3 messages in the queue. Please wait a moment and try again later.')
            return        
        else:
            q.add_msg(message)

        while not ctx.voice_client.is_playing():
            self.next(ctx, q)        


    def next(self, ctx, q):
        if len(q.queue) != 0:
            guild = ctx.guild.id
            tts = gTTS(q.queue.pop(0), lang='en') 
            tts.save(f'output-{guild}.mp3') 
            player = ctx.voice_client.play(FFmpegPCMAudio(f'output-{guild}.mp3'), after=lambda e: self.next(ctx, q))


    @commands.command()
    async def leave(self, ctx):
        if (await self.join(ctx)) == False:
            return
        if (ctx.voice_client):
            await ctx.voice_client.disconnect() 
            await ctx.send('I have left the voice channel')
        else:
            await ctx.send('I am not in a voice channel') 


    @commands.command()
    async def skip(self, ctx):
        if (await self.join(ctx)) == False:
            return
        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await ctx.send('Skipping message')


    @commands.Cog.listener()
    async def on_message(self, message):
        connection = sqlite3.connect('preferences.db')
        cursor = connection.cursor()
        # returns a cursor object that lets us use sql statements using cursor.execute()

        params = message.channel.id
        result = cursor.execute('SELECT text_channel_id FROM guilds WHERE text_channel_id=?',[params])
        channel = result.fetchone()

        if channel is None:
            return
        if not message.author.bot and not message.content.startswith(';') and message.author.voice: 
            ctx = await self.voicely.get_context(message)
            await self.join(ctx)
            await self.speak(ctx, message.content)
        connection.close()


# ask guild owner what channel voicely should listen in on.
# giuld owner picks channel. 

async def setup(client):
    await client.add_cog(voice_commands(client))
