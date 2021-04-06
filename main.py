import Client
import discord

intents = discord.Intents.default()
intents.members = True

with open("./static/token.txt") as fin:
    token = fin.read()

client = Client.Client(intents=intents)
client.run(token)