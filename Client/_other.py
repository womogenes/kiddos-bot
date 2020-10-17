import random

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