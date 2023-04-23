import discord
from discord import app_commands
from discord.ext import commands

import db
from Classes.world import World


class WorldSelect(discord.ui.Select):
    def __init__(self, idUser, targetIdUser):
        super().__init__(placeholder="Choose a world..")
        self.idUser = idUser
        self.targetIdUser = targetIdUser

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
        world = World(selected_idWorld)
        spawn_x, spawn_y = world.find_valid_spawn_position()
        db.add_user_to_world(idWorld=selected_idWorld, idUser=self.targetIdUser, x=spawn_x, y=spawn_y)
        print(f"Added new user to world with spawn position: x {spawn_x} y {spawn_y}")

class InviteView(discord.ui.View):

    def __init__(self, idUser, targetIdUser):
        super().__init__()
        self.add_item(WorldSelect(idUser=idUser, targetIdUser=targetIdUser))

class InviteCommand(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.db = client.database

    @app_commands.command(name="invite", description="Invite a player to your mini world!")
    async def invite(self, interaction: discord.Interaction, user: discord.Member):
        selected_user = user
        embed = discord.Embed(title=f"Invite {selected_user.name}",
                              description=f"Please select one of your worlds..")

        # does user have at least one world?
        if self.db.get_world_count_from_user(idUser=interaction.user.id, own_worlds_only=True) == 0:
            embed.colour = discord.Color.red()
            embed.set_footer(text="You don't have any world ready right now!")
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message(embed=embed, view=InviteView(idUser=interaction.user.id, targetIdUser=selected_user.id))

async def setup(client: commands.Bot) -> None:
    await client.add_cog(InviteCommand(client))
