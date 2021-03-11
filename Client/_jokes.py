import requests

async def tell_joke(self, message):
    if "joke" in message.content:
        joke = requests.get("https://official-joke-api.appspot.com/random_joke")
        json = joke.json()
        text = f"**{json['setup']}**\n{json['punchline']}"
        message = await message.channel.send(text)

        for emoji in ["🤬", "😕", "😐", "🤣", "🤪"]:
            await message.add_reaction(emoji)

        return True

    return False