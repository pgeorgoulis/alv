from datetime import datetime, timedelta

from discord import AllowedMentions, Embed
from discord.ext.commands import Cog
from discord.ext.commands import command


numbers = ("1️⃣", "2⃣", "3⃣", "4⃣", "5⃣",
		   "6⃣", "7⃣", "8⃣", "9⃣")


class Poll(Cog):
    def __init__(self, client):
        self.client = client

    @command(name="poll", aliases=["mkpoll", "makepoll", "createpoll"])
    async def poll(self, ctx, question, *options):
        if len(options) > 9:
            await ctx.send("You can only supply a maximum of 9 options")
        else:
            allowed_mentions = AllowedMentions(everyone=True)
            await ctx.send("@everyone new poll", allowed_mentions=allowed_mentions)
            embed = Embed(title="Poll",
                            description=question,
                            colour=0xEB459E,
                            timestamp=datetime.now())
            
            fields = [("Options", "\n".join([f"{numbers[idx]} {option}" for idx, option in enumerate(options)]), False), 
            ("Instructions", "React to cast a vote!", False)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            message = await ctx.send(embed=embed)

            for emoji in numbers[:len(options)]:
                await message.add_reaction(emoji)
            
            await ctx.message.delete()

            

async def setup(client):
    await client.add_cog(Poll(client))