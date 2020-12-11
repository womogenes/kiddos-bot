async def clear_announcements(self):
    return

    def purge(m):
        return not m.mention_everyone and m.author.id != 675191775261884436
    #print("Purging...")
    await self.announcementsChannel.purge(limit=1 << 63, check=purge)
    #print("Done purging!")
    
    
async def clean_announcements(self, message):
    return 
    
    if message.channel != self.announcementsChannel or message.mention_everyone or 763544205774815273 in [i.id for i in message.author.roles]:
        return False
        
    await message.delete()
    return True