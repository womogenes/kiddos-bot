import random
import discord
import os
import re

async def teehee(self, message):
    if message.channel.id == 763825477533302856:
        return
        
    # This is Minoo.
    if message.author.id == 722965611012948018 and message.channel != self.botChannel and message.channel != self.leaderboardChannel:
        if random.randrange(5) < 1:
            await message.channel.send("teehee :P")
            return
            
            
async def apcs(self, message):
    if re.match("ap.?cs", message.content.lower()):
        reactions = ["💻", "🤪"]
        for r in reactions:
            await message.add_reaction(r)


async def ping(self, message):
    if "<@!762164191410520094>" in message.content and message.channel != self.leaderboardChannel:
        await message.channel.send(f"<@{message.author.id}>\nRight back at you!\nUse `{self.prefix}help` for help text.")
    
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