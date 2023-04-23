import discord
from discord import app_commands
from discord.ext import commands

class LinkButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label='Invite me!', style=discord.ButtonStyle.link, url="https://discord.com/api/oauth2/authorize?client_id=1088961569431502932&permissions=2147822592&scope=bot")

    async def callback(self, interaction: discord.Interaction):

        await interaction.response.defer()

class InviteView(discord.ui.View):

    def __init__(self):
        super().__init__()
        self.add_item(LinkButton())

class BotCommand(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.db = client.database

    @app_commands.command(name="bot", description="Invite this bot to your server!")
    async def bot(self, interaction: discord.Interaction):
        embed = discord.Embed(title=f"Invite MiniMc",
                              description=f"Thanks in case you want to invite me to your server! 💕\n"
                                          f"*Don't worry!* your progress is universal!")

        await interaction.response.send_message(embed=embed, view=InviteView())

async def setup(client: commands.Bot) -> None:
    await client.add_cog(BotCommand(client))
