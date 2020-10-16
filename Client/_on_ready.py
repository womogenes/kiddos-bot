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

async def on_ready(self):
    """
    This function is called when the client is ready.
    """
    print("Logged on as " + str(self.user) + "!")
    self.initialize()
    await self.send_quote()
    await self.update_leaderboard()
    await self.replenish_cache()
    print("Question cache ready!")
    await self.clear_leaderboard()