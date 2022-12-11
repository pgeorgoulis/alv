import aiohttp
from discord import AllowedMentions, Embed
from discord.ext.commands import Cog
from discord.ext.commands import command

import random
from dotenv import load_dotenv
import asyncpraw
import os
import pprint

class Meme(Cog):
    def __init__(self, client):
        self.client = client

    @command(name="meme")
    async def mpam(self, ctx):
        load_dotenv()
        
        client_id = os.getenv('CLIENT_ID')
        client_secret = os.getenv('CLIENT_SECRET')
        password = os.getenv('PASSWORD')
        user_agent  = os.getenv('USER_AGENT')
        username  = os.getenv('U_NAME')
               
        reddit = asyncpraw.Reddit(client_id=client_id,
                                    client_secret=client_secret,
                                    password=password,
                                    user_agent=user_agent,
                                    username=username,)

        sub = await reddit.subreddit("dndmemes")
        top = sub.top(limit=20)
        all_memes = []
        async for submission in top:
            all_memes.append(submission)
        
        random_meme = random.choice(all_memes)
        #TODO there is probably a better way to do this
        if random_meme.post_hint != 'image':
            while random_meme.post_hint != 'image':
                random_meme = random.choice(all_memes)


        title = random_meme.title
        url=random_meme.url
        embed = Embed(title=title, url=url)
        embed.set_image(url=url)
        await ctx.send(embed=embed)

async def setup(client):
    await client.add_cog(Meme(client))


                #async with cs.get('https://www.reddit.com/r/dankmemes/new.json?sort=hot') as r: