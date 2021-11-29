import discord
from discord.ext import commands

class Add_date(commands.Cog):

    def __init__(self, client):
        self.client = client

    #Use add date to add a available date as a user
    @commands.command()
    async def add_date(self, ctx):
        await ctx.send('Enter the available days: ')

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        try:
            #Read the user input and split it into seperate days
            msg = await client.wait_for("message", check=check, timeout=30)
            dates_list = msg.content.lower().split(",")
            author = str(msg.author)

            matched_pattern, formated_data = format_input(dates_list)
            if matched_pattern:
                writeFile(author, formated_data)
            else:
                await ctx.send("Wrong format of data. Use !help to find the correct one")

        except asyncio.TimeoutError:
            await ctx.send("Sorry, you didn't reply in time")



    #write the dates to a csv file
    def writeFile(author, content):
        lines = list()
        found_flag=False

        with open(file_name, 'r', newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter=",")

            #Load the whole file in lines list
            for row in reader:
                name = row[0]
                print(name)
                #rows.append(row)
                if author != name:
                    lines.append(row)
                else:
                    #get the line and append it at the end
                    for string in content:
                        row.append(string)
                    lines.append(row)
                    found_flag = True
                    print("found", author)

            #If the user does not exist already
            if not found_flag:
                #then add the new user
                print("not found", author)
                content.insert(0, author)
                lines.append(content)

        #Rewrite the new file
        with open(file_name, 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(lines)

        return


def setup(client):
    client.add_cog(Add_date(client))
