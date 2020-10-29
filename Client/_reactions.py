import re
import json
from discord.utils import get

with open("./static/reactions.json", encoding="utf-8") as fin:
    reactions = json.load(fin)

async def react(self, message):
    for i in reactions:
        regex = i["regex"]
        rs = i["reactions"]
        if re.search(regex, message.content.lower()):
            for emoji in rs:
                if ":" in emoji:
                    emoji = get(self.guilds[0].emojis, name=emoji[1:-1])
                await message.add_reaction(emoji)