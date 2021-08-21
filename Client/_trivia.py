import discord

import random
import os
import time
import json
import requests

from html import unescape
from tabulate import tabulate


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
        print(f"RIGHT ANSWER: {self.rightAnswer}")
        self.answers = [unescape(i).strip()
                        for i in q["incorrect_answers"] + [self.rightAnswer]]
        allNumeric = True
        for i in self.answers:
            allNumeric = allNumeric and i.isnumeric()
        if allNumeric:
            self.answers = [str(i) for i in sorted([int(j)
                                                    for j in self.answers])]
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
        # await self.botChannel.send("There is currently no active question.\nUse `-t` for a new trivia question.")
        return

    if len(message.content) < 4:
        return

    answer = message.content[3:]
    if answer.isdigit() and 1 <= int(answer) <= len(self.answers):
        correct = self.answers[int(answer) - 1] == self.rightAnswer
    else:
        return

    self.answered = True

    if correct:
        await message.add_reaction("🧠")
        self.give_points(message.author.id, self.questionPoints)
        x = self.db.users.find_one({"idx": message.author.id})

        x["hitrate"][0] += 1
        x["hitrate"][1] += 1
        x["streak"] += 1
        self.db.users.update_one({"idx": message.author.id}, {"$set": x})

        await message.channel.send(f"""Correct! 😀 {message.author.display_name} now has **{self.get_attrib(message.author.id, 'lifetime')}** points. (+{self.questionPoints})""")
        if x["streak"] % 5 == 0:
            await message.channel.send(f"""You are on a streak of **{x["streak"]}** questions! +{x["streak"]} points!""")
            self.give_points(message.author.id, x["streak"])

    else:
        await message.add_reaction("☹️")
        self.lostPoints = -1
        self.give_points(message.author.id, self.lostPoints)

        x = self.db.users.find_one({"idx": message.author.id})
        x["hitrate"][1] += 1
        x["streak"] = 0
        self.db.users.update_one({"idx": message.author.id}, {"$set": x})

        await message.channel.send(f"""Sorry, {message.author.display_name} ️☹️ The right answer was **{self.rightAnswer}**.
{message.author.display_name} now has **{self.get_attrib(message.author.id, 'lifetime')}** points. ({self.lostPoints})""")

    await self.update_leaderboard()
