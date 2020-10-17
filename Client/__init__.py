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

class Client(discord.Client):
    
    from ._on_ready import on_ready
    from ._on_message import on_message
    from ._send_quote import send_quote
    from ._trivia import replenish_cache, send_trivia, answer_trivia
    from ._leaderboard import clear_leaderboard, clean_leaderboard, update_leaderboard
    from ._other import teehee, ping, gpt2_chat, logout
    from ._points import give_points, donate_points, balance
    from ._inherited import fetch_user
    from ._profanity import shit
    
    def initialize(self):
        with open("./data/date-info.json") as fin:
            self.dateInfo = json.load(fin)
            self.lastSent = dt.strptime(self.dateInfo["last-sent-quote"], "%Y-%m-%d %H:%M:%S.%f")
            fin.close()
            
        with open("./data/trivia-info.json") as fin:
            self.triviaInfo = json.load(fin)
            fin.close()
        
        with open("./data/point-info.json") as fin:
            x = json.load(fin)
            self.points = {"lifetime": {}, "weekly": {}, "hitrate": {}}
            for i in x["lifetime"]:
                self.points["lifetime"][int(i)] = x["lifetime"][i]
            for i in x["weekly"]:
                self.points["weekly"][int(i)] = x["weekly"][i]
            for i in x["hitrate"]:
                self.points["hitrate"][int(i)] = x["hitrate"][i]
            fin.close()
        
        # Reset weekly points on a ?day.
        if dt.now().weekday() == 0 and dt.strptime(self.dateInfo["last-reset-weekly-points"], "%Y-%m-%d %H:%M:%S.%f").date() != dt.now().date():
            for i in self.points["weekly"]:
                self.points["weekly"][i] = 0
            with open("./data/point-info.json", "w") as fout:
                json.dump(self.points, fout, indent=2)
                fout.close()
            self.dateInfo["last-reset-weekly-points"] = str(dt.now())
            with open("./data/date-info.json", "w") as fout:
                json.dump({ "last-sent-quote": str(self.lastSent) }, fout, indent=2)
                fout.close()
        
        
        self.questionCache = []
        
        self.question = None
        self.answers = None
        self.rightAnswer = None
        self.answered = True
        self.lastSentQuestion = 0
        self.lastUpdatedLeaderboard = 0
        
        self.botChannel = self.get_channel(762173542233407528)
        self.quoteChannel = self.get_channel(761340228450910250)
        self.leaderboardChannel = self.get_channel(763825477533302856)
        self.userCache = {}
