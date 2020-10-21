import json

def give_points(self, userID, points):
    if userID not in self.points["lifetime"]:
        self.points["lifetime"][userID] = 0
        self.points["weekly"][userID] = 0
        self.points["hitrate"][userID] = [0, 0]
    self.points["lifetime"][userID] += points
    self.points["weekly"][userID] += points
    
    with open("./data/point-info.json", "w") as fout:
        json.dump(self.points, fout, indent=2)
        

async def balance(self, message):
    if message.author.id not in self.points["lifetime"]:
        await message.channel.send(f"**{message.author.display_name}** does not have any points.")
        
    await message.channel.send(f"**{message.author.display_name}** has **{self.points['lifetime'][message.author.id]}** points.")
    
    
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
    await message.channel.send(f"**{user.display_name}**, you have been rewarded **{amount}** points! You now have **{self.points['lifetime'][idx]}** points.")
    
    
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
    
    if message.author.id not in self.points["lifetime"]:
        await message.channel.send(f"**{message.author.display_name}**, you do not have any points!")
        return
        
    if self.points["lifetime"][message.author.id] < 0:
        await message.channel.send(f"**{message.author.display_name}**, you are in debt with {self.points['lifetime'][message.author.id]} points. :frowning2:")
        return
        
    if amount < 0:
        await message.channel.send(f"**Nice try, {message.author.display_name}** 😉")
    
    if amount > self.points["lifetime"][message.author.id]:
        short = amount - self.points["lifetime"][message.author.id]
        await message.channel.send(f"**{message.author.display_name}**, you have **{self.points['lifetime'][message.author.id]}** points, which is **{amount - self.points['lifetime'][message.author.id]}** points short of **{amount}**. :frowning2:")
        return
    
    idx = int(idx)
    try:
        user = await self.fetch_user(idx)
    except:
        return
    
    self.give_points(idx, amount)
    self.give_points(message.author.id, -amount)
    
    await message.channel.send(f"**{message.author.display_name}** now has **{self.points['lifetime'][message.author.id]}** points and **{user.display_name}** now has **{self.points['lifetime'][idx]}** points.")
    await self.update_leaderboard()
    return