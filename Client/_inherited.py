import asyncio
import discord

async def fetch_user(self, idx):
    if idx in self.userCache:
        return self.userCache[idx]
    x = await self.guilds[0].fetch_member(idx)
    self.userCache[idx] = x
    return x