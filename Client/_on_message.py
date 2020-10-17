from datetime import datetime as dt

async def on_message(self, message):
    clippedMessage = message.content if len(message.content) < 32 else message.content[:32]
    print(str(message.author).ljust(32) + "> " + clippedMessage.ljust(40) + " " + str(dt.now()))
    
    channel = message.channel
    text = message.content
    
    if message.author == self.user:
        return
        
    # Do commands!
    if channel.id == 762173542233407528 and text.lower().strip() == "-t":
        await self.send_trivia()
        return
        
    if channel.id == 762173542233407528 and text.lower().startswith("-a "):
        await self.answer_trivia(message)
        return
        
    if text.lower().startswith("-donate "):
        await self.donate_points(message)
        return
        
    if text.lower() == "-kill" and message.author.id == 709796562733105154:
        await self.logout(message)
        return
        
    if text.lower().startswith("-balance"):
        await self.balance(message)
        return
    
    await self.clean_leaderboard(message)
    if await self.teehee(message): return
    if await self.ping(message): return