# This example requires the 'members' privileged intents

import Client

with open("./static/token.txt") as fin:
    token = fin.read()

client = Client.Client()
client.run(token)