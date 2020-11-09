async def clear_announcements(self):
    async for m in self.announcementsChannel.history():
        if not m.mention_everyone and not 763544205774815273 in [i.id for i in m.author.roles]:
            await m.delete()
    
    
async def clean_announcements(self, message):
    if message.channel != self.announcementsChannel or message.mention_everyone or 763544205774815273 in [i.id for i in message.author.roles]:
        return False
        
    await message.delete()
    return True