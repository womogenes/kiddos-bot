import os
import discord

async def logout(self, message):
    await message.channel.send("""These are my last words, and I am certain that my sacrifice will not be in vain. I am certain that, at the very least, it will be a moral lesson that will punish felony, cowardice and treason. 💀⚰️""")
    await self.commit(message, "This commit was triggered by the kill command")
    await discord.Client.logout(self)
    

async def commit(self, message, description, verbose=False):
    messages = ["Tracking files...", "Committing...", "Pushing to origin...", "Done!"]
    async def send(i):
        if verbose: await message.channel.send(messages[i])
    await send(0)
    os.system("git add .")
    await send(1)
    os.system(f'git commit -m "{description}"')
    await send(2)
    os.system("git push")
    await send(3)