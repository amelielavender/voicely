import discord
from discord.ext import commands
from queue import Queue
from typing import Dict


class TTSq:
    def __init__(self, id: int): # the only thing we need to pass in is an id variable. we annotate with the colon after the variable name.
        self.id = id
        self.queue = Queue(maxsize=3) # queue variable, type of Queue's max size 

    def add_msg(self, msg):
        self.queue.put(msg)

    @property
    def is_full(self):
        return self.queue.full()


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

        guild = ctx.guild.id
        q = self.queues.get(guild, TTSq(guild)) # get current guild's queue from qs Dict
        self.queues[guild] = q # assign q's value to qs[guild]'s key

        user = ctx.message.author.display_name 

        # concatenate name and msg received as arg
        message = '{} said: {}'.format(user, arg) 
        await ctx.send(message)
        if q.is_full:
            await ctx.send('Cannot have more than 3 messages in the queue. Please wait a moment and try again later.')
            return        
        else:
            q.add_msg(message)
            await ctx.send(q.queue.get() + ' get()')



    @commands.command()
    async def leave(self, ctx):
        if (ctx.voice_client):
            await ctx.voice_client.disconnect() 
            await ctx.send('I have left the voice channel')
        else:
            await ctx.send('I am not in a voice channel') 


async def setup(client):
    await client.add_cog(voice_commands(client))
