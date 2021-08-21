from datetime import datetime as dt
import random
import time


async def _on_message(self, message):
    clippedMessage = message.content if len(
        message.content) < 32 else message.content[:32]
    print(str(message.author).ljust(32) + "> " +
          clippedMessage.ljust(40) + " " + str(dt.now()))

    channel = message.channel
    text = message.content

    if message.author == self.user:
        return

    # Do commands!
    if channel.id == 762173542233407528 and text.lower().strip() == f"{self.prefix}t":
        await self.send_trivia()
        return

    if channel.id == 762173542233407528 and text.lower().startswith(f"{self.prefix}a "):
        await self.answer_trivia(message)
        return

    if channel.id == 762173542233407528 and text.lower().startswith(f"{self.prefix}donate "):
        await self.donate_points(message)
        return

    if text.lower().startswith(f"{self.prefix}balance"):
        await self.balance(message)
        return

    if text.lower().startswith(f"{self.prefix}help"):
        await self.send_help_text(message)
        return

    if text.lower().startswith(f"{self.prefix}skip"):
        await self.stop_music()
        return

    # Me-specific commands!
    if 827572050356731924 in [i.id for i in message.author.roles]:
        if text.lower() == f"{self.prefix}kill":
            await self.logout(message)
            return

        if text.lower().startswith(f"{self.prefix}commit "):
            await self.commit(message, message.content.split(" ", 1)[1], verbose=True)
            return

        if text.lower().startswith(f"{self.prefix}reward "):
            await self.reward(message)
            return

        if channel.id == 774135689163440188 and text.lower().startswith(f"{self.prefix}purge "):
            await self.clear_announcements(message)

        if str(dt.now().date()) == "2021-04-01" and text.lower().startswith("let the fun begin!"):
            await message.channel.send("hehehehe")
            await self.april_fools()

        if message.content == "woop woooop":
            await self.gratitude_reminder()

    if await self.clean_leaderboard(message):
        return
    if await self.clean_announcements(message):
        return
    await self.react(message)
    # if await self.teehee(message): return
    if await self.ping(message):
        return
    if await self.tell_joke(message):
        return
    if await self.fsm_picture(message):
        return

    if str(dt.now().date()) == "2021-04-01" and random.randrange(10) < 1:
        await self.random_reaction(message)

    # Spellcheck last of all because it is
    if channel.id == 807455198480957500:
        await self.spellcheck(message)
        return
