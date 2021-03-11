async def on_raw_reaction_add(self, payload):
    channel = self.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)

    await channel.send(f"Hey looks like you reacted with {payload.emoji}")