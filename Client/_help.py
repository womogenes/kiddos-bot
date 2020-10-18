import discord

async def send_help_text(self, message):
    embed = discord.Embed(title="Title", description="Description", color=0x808080)
    embed.add_field(name="Field1", value="hi", inline=True)
    embed.add_field(name="Field2", value="hi2", inline=True)
    await message.channel.send(embed=embed)