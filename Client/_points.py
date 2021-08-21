import json


def give_points(self, userID, points):
    info = self.db.users.find_one({"idx": userID})
    if not info:
        info = {
            "idx": userID,
            "lifetime": 0,
            "weekly": 0,
            "hitrate": [0, 0],
            "streak": 0
        }
        self.db.users.insert_one(info)
    info["lifetime"] += points
    info["weekly"] += points
    self.db.users.update_one({"idx": userID}, {"$set": info})


async def balance(self, message):
    if not self.db.users.find_one({"idx": message.author.id}):
        await message.channel.send(f"**{message.author.display_name}**, yo do not have any points.")

    await message.channel.send(f"**{message.author.display_name}** has **{self.get_attrib(message.author.id, 'lifetime')}** points.")


async def reward(self, message):
    text = message.content.split(" ")
    if len(text) != 3:
        return
    if len(text[1]) < 5:
        return
    idx = text[1][3:-1]
    if not idx.isnumeric():
        return
    amount = text[2]
    if not amount.isnumeric():
        return
    amount = int(amount)

    idx = int(idx)
    try:
        user = await self.fetch_user(idx)
    except:
        return

    self.give_points(idx, amount)
    await message.channel.send(f"**{user.display_name}**, you have been rewarded **{amount}** points! You now have **{self.get_attrib(idx, 'lifetime')}** points.")


async def donate_points(self, message):
    text = message.content.split(" ")
    if len(text) != 3:
        return
    if len(text[1]) < 5:
        return
    idx = text[1][3:-1]
    if not idx.isnumeric():
        return
    amount = text[2]
    if not amount.isnumeric():
        return
    amount = int(amount)

    if not self.get_attrib(message.author.id):
        await message.channel.send(f"**{message.author.display_name}**, you do not have any points!")
        return

    if self.get_attrib(message.author.id, 'lifetime') < 0:
        await message.channel.send(f"**{message.author.display_name}**, you are in debt with {self.get_attrib(message.author.id, 'lifetime')} points. :frowning2:")
        return

    if amount < 0:
        await message.channel.send(f"**Nice try, {message.author.display_name}** 😉")

    if amount > self.get_attrib(message.author.id, 'lifetime'):
        short = amount - self.get_attrib(message.author.id, 'lifetime')
        await message.channel.send(f"**{message.author.display_name}**, you have **{self.get_attrib(message.author.id, 'lifetime')}** points, which is **{amount - self.get_attrib(message.author.id, 'lifetime')}** points short of **{amount}**. :frowning2:")
        return

    idx = int(idx)
    try:
        user = await self.fetch_user(idx)
    except:
        return

    self.give_points(idx, amount)
    self.give_points(message.author.id, -amount)

    await message.channel.send(f"**{message.author.display_name}** now has **{self.get_attrib(message.author.id, 'lifetime')}** points and **{user.display_name}** now has **{self.get_attrib(idx, 'lifetime')}** points.")
    await self.update_leaderboard()
    return
