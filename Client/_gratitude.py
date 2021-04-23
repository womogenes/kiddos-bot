import time
import sched
import asyncio

async def send_reminder(self):
    print("Sending reminder...")
    await self.gratitudeChannel.send("\n".join([
        "<@!675191775261884436>",
        "<@!592819478807445504>",
    ]) + 
    "\nWhat's something you're grateful for today?")

async def gratitude_reminder(self):
    while True:
        print("Sending reminder...")
        await self.send_reminder()
        await asyncio.sleep(2 * 60 * 60)