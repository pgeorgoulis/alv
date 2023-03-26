from discord.ext.commands import command
from discord.ext.commands import Cog
from discord import app_commands
import discord
import utils

class Pictures_in_Channel(Cog):
    
    def __init__(self, client):
        self.client = client

    @app_commands.command(name="pics", description="Posts the images contained in the last `limit` messages. The default value for limit is 10000")
    async def pics(self, interaction: discord.Interaction, limit: int= None):
        if limit == None:
            limit = 10000
        else:
            if utils.is_number(limit):
                limit = int(limit)
            else:
                await interaction.channel.send("Warning: Given limit value is not valid. The command will proceed with the default limit value")
                limit = 10000

        counter = 0
        pic_counter =0
        pic_list = []
        await interaction.channel.send("Searching...", delete_after=15)
        async for message in interaction.channel.history(limit=limit):
            counter += 1
            atm_list = message.attachments
            if len(atm_list) != 0:
                for atm in atm_list:
                    atm_type = atm.content_type.split("/")[0]
                    if atm_type == 'image':
                        pic_counter += 1
                        pic_list.append(atm)

        thread = await interaction.channel.create_thread(name="Channel images",
                                                    auto_archive_duration=60,
                                                    type = discord.ChannelType.public_thread)
        await thread.send("Behold! My pics.")
        i = 0
        for pic in reversed(pic_list):
            await thread.send(pic.url)

        await interaction.response.send_message(f'{pic_counter} pics found in the last {counter} messages', delete_after = 10)

async def setup(client):
    await client.add_cog(Pictures_in_Channel(client))