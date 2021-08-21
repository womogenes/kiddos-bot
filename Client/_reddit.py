import praw
import asyncio


def login_reddit(self):
    self.reddit = praw.Reddit(username="kiddos-bot",
                              password="myverysecurepassword",
                              client_id="5S_PEqHNDiYvEQ",
                              client_secret="KLAulQ3ZigeMD7vYjoqfj6Aool0VlQ",
                              user_agent="discord:5S_PEqHNDiYvEQ:1.0 (by u/kiddos-bot)")

    print("Logged into Reddit!")

    asyncio.ensure_future(self.post_pictures())


async def post_pictures(self):
    while True:
        submission = self.reddit.subreddit("awww").random().url
        await self.redditChannel.send(submission)

        await asyncio.sleep(3600)
