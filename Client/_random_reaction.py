from ._emojis import random_emoji

async def random_reaction(self, message):
    emoji = random_emoji()
    print(emoji)
    await message.add_reaction(emoji[0])