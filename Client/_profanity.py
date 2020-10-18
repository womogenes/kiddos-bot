import re

async def shit(self, message):
    if re.match("sh(i|!|l|1)t", message.content.lower()):
        await message.add_reaction("💩")
        return