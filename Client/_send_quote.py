import time
import json
from datetime import datetime as dt
import requests


async def send_quote(self):
    if dt.strptime(next(self.db.dateInfo.find({}))["last-sent-quote"], "%Y-%m-%d %H:%M:%S.%f").date() != dt.now().date():
        url = "https://zenquotes.io/api/today"
        headers = {
            "content-type": "application/json"
        }

        info = requests.get(url, headers=headers).json()[0]
        print(info)

        quote = info["q"]
        author = info["a"]

        # Spammy quotes!
        await self.quoteChannel.send(f"""**Quote of the day:**\n\n> {quote}\n\n~ *{author}*""")

        self.db.dateInfo.update_one(
            {}, {"$set": {"last-sent-quote": str(dt.now())}})
