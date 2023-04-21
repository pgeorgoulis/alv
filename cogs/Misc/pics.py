from discord.ext.commands import command
from discord.ext.commands import Cog
from discord import app_commands
import discord
import utils

class Pictures_in_Channel(Cog):
    """"Sends all the pictures sent to this chanell in the last 10.000 messages"""

    COG_EMOJI = ":spiral_notepad:"

    
    def __init__(self, client):
        self.client = client

    @app_commands.command(name="pics", description="Posts the images contained in the last `limit` messages. The default value for limit is 10000")
    async def pics(self, interaction: discord.Interaction, limit: int= None):
        if limit == None:
            limit = 10000

        counter = 0
        pic_counter =0
        pic_list = []
        await interaction.response.send_message("Searching...")
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

        await interaction.channel.send(f'{pic_counter} pics found in the last {counter} messages', delete_after = 10)

    @app_commands.command(name="files", description="Posts the files contained in the last `limit` messages. The default value for limit is 10000")
    async def files(self, interaction: discord.Interaction, limit: int= None):
        if limit == None:
            limit = 10000

        counter = 0
        pic_counter =0
        pic_list = []
        await interaction.response.send_message("Searching...")
        async for message in interaction.channel.history(limit=limit):
            counter += 1
            atm_list = message.attachments
            if len(atm_list) != 0:
                for atm in atm_list:
                    atm_type = atm.content_type.split("/")[0]
                    if atm_type == 'application' or atm_type == 'text':
                        pic_counter += 1
                        pic_list.append(atm)

        thread = await interaction.channel.create_thread(name="Channel files",
                                                    auto_archive_duration=60,
                                                    type = discord.ChannelType.public_thread)
        await thread.send("Behold! My files.")
        i = 0
        for pic in reversed(pic_list):
            await thread.send(pic.url)

        await interaction.channel.send(f'{pic_counter} files found in the last {counter} messages', delete_after = 10)

async def setup(client):
    await client.add_cog(Pictures_in_Channel(client))