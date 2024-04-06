import discord
from discord import app_commands
from discord.ext import commands
from Classes import World
from Classes import WorldHasUsers
from session import session, Session


class AddPlayerCommand(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="addplayer", description="Add another player to any of your worlds.")
    async def addPlayerCommand(self, interaction: discord.Interaction, user: discord.Member):
        await interaction.response.defer()
        user_id = interaction.user.id

        embed = discord.Embed(title=f"Adding {user.name} to world..",
                              description=f"Please select one of your worlds..")

        # create a new session for this request
        session = Session()

        try:
            # get player worlds
            worlds = session.query(World).join(World.users).filter(WorldHasUsers.user_id == user_id).all()

            if not worlds:
                embed.colour = discord.Color.red()
                embed.set_footer(text="You don't have any world ready right now! You can create one with /generate")
                await interaction.followup.send(embed=embed)
            else:
                await interaction.followup.send(embed=embed, view=WorldSelectionView(user_id=user_id, worlds=worlds, add_player_user=user))

            session.commit()
        except Exception as e:
            # rollback the transaction if an error occurs
            session.rollback()
            raise e
        finally:
            # close the session
            session.close()


async def setup(client: commands.Bot) -> None:
    await client.add_cog(AddPlayerCommand(client))

class WorldSelectionView(discord.ui.View):
    def __init__(self, user_id, worlds, add_player_user):
        super().__init__()

        self.add_item(WorldSelect(user_id=user_id, worlds=worlds, add_player_user=add_player_user))

class WorldSelect(discord.ui.Select):
    def __init__(self, user_id, worlds, add_player_user):
        super().__init__(placeholder="Choose a world..")
        self.user_id = user_id
        self.worlds = worlds
        self.add_player_user = add_player_user

        for world in self.worlds:
            self.add_option(label=f"{world.name}", value=f"{world.id}", emoji="🌎")

    async def callback(self, interaction: discord.Interaction):
        world_id = self.values[0]

        exist_in_world = session.query(WorldHasUsers)\
            .filter(WorldHasUsers.user_id == self.add_player_user.id)\
            .filter(WorldHasUsers.world_id == world_id).first()

        if not exist_in_world:
            world = session.query(World).filter(World.id == world_id).first()

            world.spawn_player(session=session, user_id=self.add_player_user.id)

            message = interaction.message
            edited_embed = message.embeds[0]
            edited_embed.colour = discord.Color.green()
            edited_embed.set_footer(text=f"Added {self.add_player_user.name} to the world!")

            return await interaction.message.edit(embed=edited_embed, view=None)
        else:
            # user already exists in the world
            message = interaction.message
            edited_embed = message.embeds[0]
            edited_embed.colour = discord.Color.red()
            edited_embed.set_footer(text=f"{self.add_player_user.name} is already inside the world!")

            return await interaction.message.edit(embed=edited_embed, view=None)