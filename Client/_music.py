import asyncio
import youtube_dl
import discord
import random
import os
from os import path
import datetime as dt
import time
from urllib.error import HTTPError
import subprocess

from pprint import pprint

youtube_dl.utils.bug_reports_message = lambda: ""

ytdl_format_options = {
    "format": "bestaudio/best",
    "outtmpl": "%(extractor)s-%(id)s-%(title)s.%(ext)s",
    "restrictfilenames": True,
    "noplaylist": True,
    "nocheckcertificate": True,
    "ignoreerrors": False,
    "logtostderr": False,
    "quiet": True,
    "no_warnings": True,
    "default_search": "auto",
    "source_address": "0.0.0.0" # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    "options": "-vn"
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get("title")
        self.url = data.get("url")

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        def get_length(input_video):
            result = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", input_video], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            return float(result.stdout)

        """
        videoID = url[url.index("v=") + 2:]
        filename = ""
        for name in os.listdir():
            if videoID in name:
                filename = name

                break

        if filename == "":
            return None
        """

        #"""
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        
        if "entries" in data:
            # Take first item from a playlist
            data = data["entries"][0]

        filename = data["url"] if stream else ytdl.prepare_filename(data)
        data = {
            'duration': get_length(filename)
        }
        #"""
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data), data


def to_title(s):
    return " ".join([c[0].upper() + c[1:] for c in s.split(" ")])

async def music(self):
    self.playlist = []
    with open("./static/playlist.txt") as fin:
        fin.readline() # Header
        x = fin.readline()
        while x:
            k = x.split("\t")
            if len(k[1]) > 0:
                self.playlist.append(k)
            x = fin.readline()

    self.vc = self.get_channel(768985179473444925)
    self.voice = await self.vc.connect()

    await self.guilds[0].change_voice_state(channel=self.vc, self_deaf=True)

    print("Connected to voice channel!")

    asyncio.ensure_future(self.play_music())
    asyncio.ensure_future(self.flash_music_embed())


async def stop_music(self):
    await self.songEmbedMessage.delete()
    self.songEmbedMessage = None

    self.voice.stop()


async def flash_music_embed(self):
    while True:
        if self.songEmbedMessage:
            try:
                embed = self.songEmbedMessage.embeds[0]
                if embed.color.value == 0x3f9137:
                    color = 0xff0000
                else:
                    color = 0x3f9137
                #print("color", color)
                embed = discord.Embed(title=embed.title, description=embed.description, color=color)
                await self.songEmbedMessage.edit(embed=embed)

            except:
                pass

        await asyncio.sleep(2)


async def play_music(self):
    while True:
        """
        if not self.voice.is_connected():
            try:
                self.voice = await self.vc.connect()
            except:
                pass
        """
        if not self.voice.is_connected():
            print("Not connected, reconnecting...")
            await self.voice.connect(timeout=60, reconnect=True)
            print("Reconnected!")

        if not self.voice.is_playing():
            while True:
                os.chdir(path.join(self.dir, "temp"))

                try:
                    x = None
                    while not x:
                        song = random.choice(self.playlist)
                        url = song[1].strip()
                        if url == "":
                            continue
                        x = await YTDLSource.from_url(url, loop=False, stream=False)
                        print(x, random.randrange(1, 10))
                        
                    source, data = x
                    self.voice.play(source)
                    self.songsPlayed += 1
                    
                    title = "🎅🎄 Now playing  ⛄🔥"
                    description = f"[{to_title(song[0])}]({url}) ({time.strftime('%M:%S', time.gmtime(data['duration'])) })"
                    color = 0xff0000 if self.songsPlayed % 2 else 0x3f9137
                    self.musicEmbed = discord.Embed(title=title, description=description, color=color)

                    if self.songEmbedMessage:
                        await self.songEmbedMessage.delete()
                    self.songEmbedMessage = await self.musicChannel.send(embed=self.musicEmbed)

                    break
                
                except HTTPError as error:
                    print("eeeeeeeeeeeeeeeeeerror", error)
                    print("rrrrrrrrrrrrrrrrraw", error.raw)
                    await self.musicChannel.send("Technical difficulties, retrying in a minute.")
                    await asyncio.sleep(60 * 10)

                except youtube_dl.utils.DownloadError as error:
                    print("song:", song)
                    print("url:", url)
                    print("#ERROR")
                    print(error)
                    print("#ERROR")
                    await self.musicChannel.send("Technical difficulties, retrying in a minute.")
                    await asyncio.sleep(60 * 10)

                os.chdir(self.dir)

            os.chdir(self.dir)

        await asyncio.sleep(1)