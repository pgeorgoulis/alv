from discord import Embed
from discord.ext.commands import Cog
from discord import app_commands
import discord
import random
from dotenv import load_dotenv
import asyncpraw
import os


class Meme(Cog):
    """Sends a meme from the top posts 35 in r/dndmemes from the last week"""
    
    COG_EMOJI = "💀"


    def __init__(self, client):
        self.client = client

    @app_commands.command(name="meme", description="Posts a meme from the r/dndmemes subreddit")
    async def meme(self, interaction: discord.Interaction):
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
        top = sub.top("week",limit=35)
        all_memes = []
        async for submission in top:
            all_memes.append(submission)
        
        random_meme = random.choice(all_memes)

        #TODO there is probably a better way to do this
        if random_meme.post_hint != 'image':
            #Confirm that the post is an image and not text, gif or a video
            while random_meme.post_hint != 'image':
                random_meme = random.choice(all_memes)

        title = random_meme.title
        url=random_meme.url
        embed = Embed(title=title, url=url)
        embed.set_image(url=url)
        await interaction.response.send_message(embed=embed)

async def setup(client):
    await client.add_cog(Meme(client))
