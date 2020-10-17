import random
import discord
import os

async def logout(self, message):
    await message.channel.send("""These are my last words, and I am certain that my sacrifice will not be in vain. I am certain that, at the very least, it will be a moral lesson that will punish felony, cowardice and treason. 💀⚰️""")
    os.system("git add .")
    os.system('git commit -m "Make sure to save the points file!"')
    os.system("git push")
    await discord.Client.logout(self)
    

async def teehee(self, message):
    if message.channel.id == 763825477533302856:
        return
        
    # This is Minoo.
    if message.author.id == 722965611012948018 and message.channel != self.botChannel and message.channel != self.leaderboardChannel:
        if random.randrange(5) < 1:
            await message.channel.send("teehee :P")
            return


async def ping(self, message):
    if "<@!762164191410520094>" in message.content and message.channel != self.leaderboardChannel:
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