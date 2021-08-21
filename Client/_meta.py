import os
import discord


async def logout(self, message):
    if message.author.id != 675191775261884436:
        return

    await message.channel.send("""These are my last words, and I am certain that my sacrifice will not be in vain. I am certain that, at the very least, it will be a moral lesson that will punish felony, cowardice and treason. 💀⚰️""")
    await self.commit(message, "This commit was triggered by the kill command")
    await discord.Client.logout(self)


async def commit(self, message, description, verbose=False):
    steps = [
        ["git add .", "Tracking files..."],
        [f"git commit -m {description}", "Committing..."],
        ["git push", "Pushing to origin..."],
        ["", "Done"]
    ]
    for command, message in steps:
        if verbose:
            await message.channel.send(message)
        os.system(command)
