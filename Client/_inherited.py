import asyncio
import discord

async def fetch_user(self, idx):
    if idx in self.userCache:
        return self.userCache[idx]
    x = await discord.Client.fetch_user(self, idx)
    self.userCache[idx] = x
    return x