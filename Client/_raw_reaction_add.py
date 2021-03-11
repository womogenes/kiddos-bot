async def on_raw_reaction_add(self, payload):
    if payload.user_id == self.user.id:
        return

    emoji = payload.emoji
    channel = self.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)

    print(emoji, type(emoji), emoji == "❓")

    if str(emoji) == "❓":
        print("asdf")
        await self.tell_punchline(message)