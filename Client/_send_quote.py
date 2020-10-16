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

async def send_quote(self):
    if self.lastSent.date() != dt.now().date():
        url = 'https://quotes.rest/qod?category=inspire'
        api_token = "X-TheySaidSo-Api-Secret"
        headers = {
            "content-type": "application/json",
            "X-TheySaidSo-Api-Secret": format(api_token)
        }

        response = requests.get(url, headers=headers)
        quotes = response.json()["contents"]["quotes"][0]
        
        # Spammy quotes!
        msgId = await self.quoteChannel.send(f"""**Quote of the day:**\n\n> {quotes["quote"]}\n\n~ *{quotes["author"]}*""")

        self.dateInfo["last-sent-quote"] = str(dt.now())
        with open("./data/date-info.json", "w") as fout:
            json.dump(self.dateInfo, fout, indent=2)
            fout.close()