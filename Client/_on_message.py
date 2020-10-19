from datetime import datetime as dt

async def on_message(self, message):
    clippedMessage = message.content if len(message.content) < 32 else message.content[:32]
    print(str(message.author).ljust(32) + "> " + clippedMessage.ljust(40) + " " + str(dt.now()))
    
    channel = message.channel
    text = message.content
    
    if message.author == self.user:
        return
        
    # Do commands!
    if channel.id == 762173542233407528 and text.lower().strip() == f"{self.prefix}t":
        await self.send_trivia()
        return
        
    if channel.id == 762173542233407528 and text.lower().startswith(f"{self.prefix}a "):
        await self.answer_trivia(message)
        return
        
    if text.lower().startswith(f"{self.prefix}donate "):
        await self.donate_points(message)
        return
        
    if text.lower() == f"{self.prefix}kill" and message.author.id == 709796562733105154:
        await self.logout(message)
        return
        
    if text.lower().startswith(f"{self.prefix}balance"):
        await self.balance(message)
        return
        
    if text.lower().startswith(f"{self.prefix}help"):
        await self.send_help_text(message)
        return
    
    await self.clean_leaderboard(message)
    await self.shit(message)
    await self.fuck(message)
    if await self.teehee(message): return
    if await self.ping(message): return