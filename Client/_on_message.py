import discord
from discord.ext import commands
from discord.utils import get

import random
import sys
import os
import time
import json
from datetime import datetime as dt
import requests
from pprint import pprint

from html import unescape
from tabulate import tabulate

async def on_message(self, message):
    clippedMessage = message.content if len(message.content) < 64 else message.content[:64]
    print(str(message.author).ljust(32) + "> " + clippedMessage + " " + str(dt.now()))
    
    channel = message.channel
    text = message.content
    
    if message.author == self.user:
        return
        
    # Do commands!
    if text.lower().strip() == "-t":
        await self.send_trivia()
        return
        
    if channel.id == 762173542233407528 and text.lower().startswith("-a"):
        await self.answer_trivia(message)
        return

    await self.clean_leaderboard(message)
    if await self.teehee(message): return
    if await self.ping(message): return