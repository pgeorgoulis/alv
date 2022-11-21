import discord
from discord.ext import commands

class Pictures_in_Channel(commands.Cog):
    
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def pics(self, ctx):
        counter = 0
        pic_counter =0
        pic_list = []
        async for message in ctx.channel.history(limit=10000):
            counter += 1
            atm_list = message.attachments
            if len(atm_list) != 0:
                for atm in atm_list:
                    atm_type = atm.content_type.split("/")[0]
                    if atm_type == 'image':
                        pic_counter += 1
                        pic_list.append(atm)

        thread = await ctx.channel.create_thread(name="Pics in the channel",
                                                    type = discord.ChannelType.public_thread)
        await thread.send("This message is sent to the created thread!")
        i = 0
        for pic in pic_list:
            await thread.send(pic.url)

        await ctx.send(f'{pic_counter} pics found in the last {counter} messages')

async def setup(client):
    await client.add_cog(Pictures_in_Channel(client))