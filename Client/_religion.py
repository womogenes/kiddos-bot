async def fsm_picture(self, message):
    if message.content.lower() == "fsm":
        await message.channel.send("https://upload.wikimedia.org/wikipedia/commons/thumb/9/90/Touched_by_His_Noodly_Appendage_HD.jpg/330px-Touched_by_His_Noodly_Appendage_HD.jpg")
        return True

    return