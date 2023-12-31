from discord import FFmpegPCMAudio
from discord.ext import commands
from typing import Dict
from gtts import gTTS
import asyncio
import sqlite3
import os
import regex as re
from dotenv import load_dotenv

load_dotenv()

db = os.getenv("DATABASE")


class TTSq:
    def __init__(
        self, id: int
    ):  # the only thing we need to pass in is an id variable. we annotate with the colon after the variable name.
        self.id = id
        self.queue = []  # queue variable, q's max size will be 3

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
        self.counter = 21

    async def join(self, ctx):  # joins vc if msg author is in vc.
        author = ctx.message.author  # get msg author
        voice_chan = ctx.author.voice  # join same vs msg author is in

        if (voice_chan) and not (
            ctx.voice_client
        ):  # if user in VC and bot not in VC, join same VC
            channel = ctx.message.author.voice.channel
            await channel.connect()
        elif (voice_chan) and (ctx.voice_client):  # if already in VC, move on
            pass
        else:
            await ctx.send("You are not in a voice channel.")
            return False

    @commands.hybrid_command(description="manually invoke voicely's text-to-speech")
    async def tts(self, ctx: commands.Context, *, text: str) -> None:
        if await self.join(ctx) == False:
            return
        else:
            await self.speak(ctx, text)
        emoji = "🔊"
        try:
            await ctx.message.add_reaction(emoji)
        except:
            print("TTS invoked using slash command")
        else:
            await ctx.send(emoji, ephemeral=True)

    async def speak(self, ctx, msg):
        guild = ctx.guild.id
        q = self.queues.get(
            guild, TTSq(guild)
        )  # get current guild's queue from qs Dict
        self.queues[guild] = q  # assign q's value to qs[guild]'s key

        user = ctx.message.author.display_name

        connection = sqlite3.connect(db)
        cursor = connection.cursor()

        result = cursor.execute("SELECT x_said FROM guilds WHERE guild_id= ? ", [guild])
        xsaid = result.fetchone()

        words = msg.split()

        for i in range(len(words)):
            # A discord user ID
            raw = r"<@[0-9]*>"
            raw_emoji = r"<:.*:[0-9]*>"
            raw_url = r"(?<=https:\/\/|http:\/\/|ftp:\/\/).+?[^\/:](?=[?\/]|$)"

            res = re.search(raw, words[i])
            if res == None:
                res_emoji = re.search(raw_emoji, words[i])
                if res_emoji == None:
                    res_url = re.search(raw_url, words[i])
                    if res_url == None:
                        continue
                    else:
                        words[i] = str(res_url.group())
                elif words[i] == res_emoji.group():
                    search = r"(?<=:).+?(?=:)"
                    name = re.search(search, words[i])
                    words[i] = str(name.group())
            elif words[i] == res.group():
                id = res.group().strip("<@>")
                transform = ctx.author.guild.get_member(int(id))
                name = str(transform.display_name)
                words[i] = name

        msg = " ".join(words)

        if xsaid[0] == 1:
            # concatenate name and msg received as arg
            message = "{} said: {}".format(user, msg)
        if xsaid[0] == 0:
            message = msg
        connection.close()

        if len(ctx.message.stickers) > 0:
            sticker = ctx.message.stickers[0].name
            message = message + sticker
        if msg == "" and len(ctx.message.attachments) > 0:
            message = "{} has attached a file.".format(user)
        elif len(ctx.message.attachments) > 0:
            message = message + "{} has attached a file".format(user)

        if q.is_full:
            await ctx.send(
                "Cannot have more than 3 messages in the queue. Please wait a moment and try again later."
            )
            return
        else:
            q.add_msg(message)

        while not ctx.voice_client.is_playing():
            self.next(ctx, q)

    def next(self, ctx, q):
        if len(q.queue) != 0:
            guild = ctx.guild.id
            tts = gTTS(q.queue.pop(0), lang="en")
            outfile = f"files/tts/output-{guild}.mp3"
            tts.save(outfile)
            player = ctx.voice_client.play(
                FFmpegPCMAudio(outfile), after=lambda e: self.next(ctx, q)
            )

    @commands.hybrid_command(description="leaves the current voice channel")
    async def leave(self, ctx: commands.Context) -> None:
        if (await self.join(ctx)) == False:
            return
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await ctx.send("I have left the voice channel")
        else:
            await ctx.send("I am not in a voice channel")

    @commands.hybrid_command(description="skips the currently playing message")
    async def skip(self, ctx: commands.Context) -> None:
        if (await self.join(ctx)) == False:
            return
        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await ctx.send("Skipping message")

    @commands.Cog.listener()
    async def on_message(self, message):
        connection = sqlite3.connect(db)
        cursor = connection.cursor()
        # returns a cursor object that lets us use sql statements using cursor.execute()

        params = message.channel.id
        result = cursor.execute(
            "SELECT text_channel_id FROM guilds WHERE text_channel_id=?", [params]
        )
        channel = result.fetchone()
        ctx = await self.voicely.get_context(message)

        if channel is None:
            return
        if (
            not message.author.bot
            and not message.content.startswith(";")
            and message.author.voice
        ):
            await self.join(ctx)

            if message.content.startswith('i will kill you right now'):
                try:
                    player = ctx.voice_client.play(
                    FFmpegPCMAudio(f"files/tts/killyou.wav")
                )
                except:
                    await self.speak(ctx, message.content)
            else:  
                await self.speak(ctx, message.content)
            
            vc = ctx.guild.voice_client.channel

            # unfortunately the below block is very hacky.
            # i don't posess the necessary knowledge as a beginner.
            while True:
                await asyncio.sleep(1)
                self.counter += 1
                if self.counter >= 20 and len(vc.members) == 1:
                    await ctx.voice_client.disconnect()
                    self.counter = 0
                    return
                elif len(vc.members) > 1:
                    self.counter = 20
                    await asyncio.sleep(2)
                    pass

        connection.close()


async def setup(client):
    await client.add_cog(voice_commands(client))
