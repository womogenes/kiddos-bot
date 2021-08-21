async def clear_announcements(self, message):
    to_purge = int(message.content.split(" ")[1])

    def purge(m):
        return not (m.mention_everyone or m.author.id == 675191775261884436) or m.content.startswith("\purge ")

    print("Purging...")
    await self.announcementsChannel.purge(limit=to_purge, check=purge)
    print("Done purging!")


async def clean_announcements(self, message):
    return

    if message.channel != self.announcementsChannel or message.mention_everyone or 763544205774815273 in [i.id for i in message.author.roles]:
        return False

    await message.delete()
    return True
