import re

async def shit(self, message):
    if re.search("sh(i|\*|!|l|1)t", message.content.lower()):
        await message.add_reaction("💩")
        return
        
async def fuck(self, message):
    if re.search("f(u|\*|/|)ck", message.content.lower()):
        await message.add_reaction("🖕")
        return