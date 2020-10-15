# This example requires the 'members' privileged intents

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

import Client

import discord

ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4])
shorten = lambda x: x if len(x) < 16 else x[:13] + "..."
signify = lambda x: "+" + str(x) if x > 0 else x

class MyClient(discord.Client):
    
        
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
        if await self.gpt2_chat(message): return
        
        
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
                
                
    async def replenish_cache(self):
        amount = max(10 - len(self.questionCache), 0)
        url = f"https://opentdb.com/api.php?amount={amount}"
        response = requests.get(url)
        
        self.questionCache.extend(response.json()["results"])
        
    
    async def send_trivia(self):
        await self.replenish_cache()
        q = self.questionCache.pop(0)
        
        if self.question == None or self.answered:
            diff = q["difficulty"]
            if diff == "easy":
                self.questionPoints = 2
            elif diff == "medium":
                self.questionPoints = 3
            else:
                self.questionPoints = 4
                
            self.question = f"**Trivia question:** ({self.questionPoints} points)"
            self.question += f"\n{unescape(q['question'])}"
            
            self.rightAnswer = unescape(q["correct_answer"]).strip()
            self.answers = [unescape(i).strip() for i in q["incorrect_answers"] + [self.rightAnswer]]
            allNumeric = True
            for i in self.answers:
                allNumeric = allNumeric and i.isnumeric()
            if allNumeric:
                self.answers = [str(i) for i in sorted([int(j) for j in self.answers])]
            if len(self.answers) != 2 and not allNumeric:
                random.shuffle(self.answers)
            if len(self.answers) == 2:
                self.answers = ["True", "False"]
            self.answered = False
        
            # bot channel.
            self.question += "\n"
            for i in range(len(self.answers)):
                self.question += f"**{i + 1}**. {unescape(self.answers[i])}\n"
            await self.botChannel.send(self.question)
            self.lastSentQuestion = time.time()
            
            await self.replenish_cache()
            
        elif not self.answered and time.time() - self.lastSentQuestion > 10:
            await self.botChannel.send(self.question)
            
        
    async def answer_trivia(self, message):    
        if self.answered:
            #await self.botChannel.send("There is currently no active question.\nUse `-t` for a new trivia question.")
            return
            
        if len(message.content) < 4:
            return
        
        answer = message.content[3:]
        if answer.isdigit() and 1 <= int(answer) <= len(self.answers):
            correct = self.answers[int(answer) - 1] == self.rightAnswer
        else:
            return
            
        self.answered = True
        
        if message.author.id not in self.points["lifetime"]:
            self.points["lifetime"][message.author.id] = 0
            self.points["weekly"][message.author.id] = 0
            self.points["hitrate"][message.author.id] = [0, 0]
            
        self.points["hitrate"][message.author.id][1] += 1
        
        if correct:
            self.points["lifetime"][message.author.id] += self.questionPoints
            self.points["weekly"][message.author.id] += self.questionPoints
            self.points["hitrate"][message.author.id][0] += 1
            await self.botChannel.send(f"""Correct! 🙂 {message.author.display_name} now has **{self.points["lifetime"][message.author.id]}** points. (+{self.questionPoints})""")
            
        else:
            lostPoints = 1
            self.points["lifetime"][message.author.id] -= lostPoints
            self.points["weekly"][message.author.id] -= lostPoints
            await self.botChannel.send(f"""Sorry, {message.author.display_name} ☹ The right answer was **{self.rightAnswer}**.
{message.author.display_name} now has **{self.points["lifetime"][message.author.id]}** points. (-{lostPoints})""")
        
        with open("./data/point-info.json", "w") as fout:
            json.dump(self.points, fout, indent=2)
            fout.close()
        
        await self.update_leaderboard()
        
        
    async def clear_leaderboard(self):
        async for m in self.leaderboardChannel.history():
            if m.id != 763825813182611477:
                await m.delete()
    
    
    async def clean_leaderboard(self, message):
        if message.channel.id != 763825477533302856:
            return
            
        if message.id != 763825813182611477:
            await message.delete()
                
    
    async def update_leaderboard(self):
        message = await self.leaderboardChannel.fetch_message(763825813182611477)
        
        # By lifetime points.
        table1 = [["Rank", "Name", "Points"]]
        tp = sorted(self.points["lifetime"], key=lambda x: self.points["lifetime"][x], reverse=True)
        for i in range(len(tp)):
            user = await self.fetch_user(tp[i])
            table1.append([ordinal(i + 1), user.display_name, self.points["lifetime"][tp[i]]])
        
        text1 = tabulate(table1, headers="firstrow", tablefmt="github", numalign="left")
        
        # By weekly points.
        table2 = [["Rank", "Name", "Points"]]
        tw = sorted(self.points["weekly"], key=lambda x: self.points["weekly"][x], reverse=True)
        for i in range(len(tw)):
            user = await self.fetch_user(tw[i])
            x = self.points["weekly"][tw[i]]
            table2.append([ordinal(i + 1), user.display_name, signify(self.points["weekly"][tw[i]])])
        
        text2 = tabulate(table2, headers="firstrow", tablefmt="github", numalign="left")
        
        # By hitrate.
        table3 = [["Rank", "Name", "Correct/Total", "Accuracy"]]
        def hitrate(x):
            if self.points["hitrate"][x][1] < 10:
                return 0
            return self.points["hitrate"][x][0] / self.points["hitrate"][x][1]
            
        ac = sorted(self.points["weekly"], key=hitrate, reverse=True)
        for i in range(len(ac)):
            user = await self.fetch_user(ac[i])
            percent = 0 if self.points["hitrate"][user.id][1] == 0 else self.points["hitrate"][user.id][0] / self.points["hitrate"][user.id][1]
            percentage = str(round(percent * 100, 1)) + "%"
            outof = f"{self.points['hitrate'][user.id][0]}/{self.points['hitrate'][user.id][1]}"
            table3.append([ordinal(i + 1), user.display_name, outof, percentage])
        
        text3 = tabulate(table3, headers="firstrow", tablefmt="github", numalign="left")
        
        text = ""
        text += f"**Sorted by accuracy:**\n```{text3}```\n"
        text += f"**Sorted by lifetime points:**\n```{text1}```\n"
        text += f"**Sorted by this week's points:**\n```{text2}```\n"
        
        text = text[:-1]
        
        await message.edit(content=text)
        
        print("UPDATED LEADERBOARDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD")
        
    
    async def teehee(self, message):
        if message.channel.id == 763825477533302856:
            return
            
        # This is Minoo.
        if message.author.id == 722965611012948018 and message.channel != self.botChannel:
            if random.randrange(5) < 1:
                await message.channel.send("teehee :P")
                return
    
    
    async def ping(self, message):
        if "<@!762164191410520094>" in message.content:
            await message.channel.send(f"<@{message.author.id}>\nRight back at you!")
        
        if message.content == "ping":
            if random.randrange(10) < 1:
                await message.channel.send(":O ponggers")
                return True
        return False
    
        
    async def gpt2_chat(self, message):
        # This is the gpt2-chatbot channel.
        if not loadChatbot:
            return
            
        if message.channel.id == 762173542233407528:
            if random.randrange(5) < 1:
                async with message.channel.typing():
                    response = chatbot.get_response(message.content)
                    time.sleep(random.random() * 1)
                    await message.channel.send(response)
                    return True
        return False



client = Client.Client()
client.run('NzYyMTY0MTkxNDEwNTIwMDk0.X3lKtw.rFAjDvgtGDKi5DvnSYl0HiTu96U')