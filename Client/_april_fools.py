from discord.utils import get


async def april_fools(self):
    # April fool's
    roles = [
        get(self.guilds[0].roles, id=x)
        for x in [
            763544205774815273,  # bot developer
            780950367692128296  # the real minoo
        ]
    ]
    for member in self.guilds[0].members:
        print(f"Editing {member}...")
        try:
            await member.edit(nick="tetromino", roles=member.roles + roles)
        except:
            print("Failed")

    print("asdf", len(self.guilds[0].members))
