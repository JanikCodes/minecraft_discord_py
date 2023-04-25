import discord
from discord import app_commands
from discord.ext import commands
from Classes.world import World


class WorldSelect(discord.ui.Select):
    def __init__(self, idUser, targetIdUser, db):
        super().__init__(placeholder="Choose a world..")
        self.idUser = idUser
        self.targetIdUser = targetIdUser
        self.db = db

        for world in db.get_all_worlds_from_user(idUser=idUser, own_worlds_only=True):
            self.add_option(label=f"{world.get_name()}", description=f"size: {world.get_world_size().get_name()}", value=f"{world.get_id()}", emoji="🌎")

    async def callback(self, interaction: discord.Interaction):

        if interaction.user.id != self.idUser:
            embed = discord.Embed(title=f"You're not allowed to use this action!",
                                  description="",
                                  colour=discord.Color.red())
            return await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=2)

        await interaction.response.defer()

        selected_idWorld = self.values[0]
        world = World(selected_idWorld, db=self.db)
        spawn_x, spawn_y = world.find_valid_spawn_position()
        res = self.db.add_user_to_world(idWorld=selected_idWorld, idUser=self.targetIdUser, x=spawn_x, y=spawn_y)
        if res:
            message = interaction.message
            edited_embed = message.embeds[0]
            edited_embed.colour = discord.Color.green()
            edited_embed.set_footer(text="Added new user to world!")

            return await interaction.message.edit(embed=edited_embed, view=None)
        else:
            # no success
            message = interaction.message
            edited_embed = message.embeds[0]
            edited_embed.colour = discord.Color.red()
            edited_embed.set_footer(text="User is already allowed in world!")

            return await interaction.message.edit(embed=edited_embed)

class InviteView(discord.ui.View):

    def __init__(self, idUser, targetIdUser, db):
        super().__init__()
        self.add_item(WorldSelect(idUser=idUser, targetIdUser=targetIdUser, db=db))

class InviteCommand(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.db = client.database

    @app_commands.command(name="invite", description="Invite a player to your mini world!")
    async def invite(self, interaction: discord.Interaction, user: discord.Member):
        await interaction.response.defer()
        selected_user = user
        embed = discord.Embed(title=f"Invite {selected_user.name}",
                              description=f"Please select one of your worlds..")

        # does user have at least one world?
        if self.db.get_world_count_from_user(idUser=interaction.user.id, own_worlds_only=True) == 0:
            embed.colour = discord.Color.red()
            embed.set_footer(text="You don't have any world ready right now!")
            await interaction.followup.send(embed=embed)
        else:
            await interaction.followup.send(embed=embed, view=InviteView(idUser=interaction.user.id, targetIdUser=selected_user.id, db=self.db))

async def setup(client: commands.Bot) -> None:
    await client.add_cog(InviteCommand(client))
