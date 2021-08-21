import requests


async def tell_joke(self, message):
    if "joke" in message.content:
        joke = requests.get(
            "https://official-joke-api.appspot.com/random_joke")
        json = joke.json()
        text = f"**{json['setup']}**"
        message = await message.channel.send(text)
        self.punchlines[message.id] = json["punchline"]

        await message.add_reaction("❓")

        return True

    return False


async def tell_punchline(self, message):
    if message.id in self.punchlines:
        punchline = self.punchlines[message.id]
        del self.punchlines[message.id]
        message = await message.channel.send(punchline)

        for emoji in ["🤬", "😕", "😐", "🤣", "🤪"]:
            await message.add_reaction(emoji)
