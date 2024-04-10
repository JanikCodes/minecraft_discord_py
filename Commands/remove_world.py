import discord
from discord import app_commands
from discord.ext import commands
from sqlalchemy.orm import sessionmaker
from Classes import World, WorldHasBlocks
from Classes import WorldHasUsers
from database import engine


class RemoveWorldCommand(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="removeworld", description="Remove a world permanently")
    async def removeWorldCommand(self, interaction: discord.Interaction):
        await interaction.response.defer()
        user_id = interaction.user.id

        embed = discord.Embed(title=f"Removing a world..",
                              description=f"Please select one of your available worlds..")

        # create a new session for this request
        Session = sessionmaker(bind=engine)
        session = Session()

        try:
            # get player worlds
            worlds = session.query(World).join(World.users).filter(WorldHasUsers.user_id == user_id).all()

            if not worlds:
                embed.colour = discord.Color.red()
                embed.set_footer(text="You haven't joined any world yet. You can do so by typing /generate")
                await interaction.followup.send(embed=embed)
            else:
                await interaction.followup.send(embed=embed, view=WorldSelectionView(user_id=user_id, session=session, worlds=worlds))
            session.commit()
        except Exception as e:
            # rollback the transaction if an error occurs
            session.rollback()
            raise e
        finally:
            # close the session
            session.close()


async def setup(client: commands.Bot) -> None:
    await client.add_cog(RemoveWorldCommand(client))

class WorldSelectionView(discord.ui.View):
    def __init__(self, user_id, session, worlds):
        super().__init__()

        self.add_item(WorldSelect(user_id=user_id, session=session, worlds=worlds))

class WorldSelect(discord.ui.Select):
    def __init__(self, user_id, session, worlds):
        super().__init__(placeholder="Choose a world..")
        self.user_id = user_id
        self.session = session
        self.worlds = worlds

        for world in self.worlds:
            self.add_option(label=f"{world.name}", value=f"{world.id}", emoji="🌎")

    async def callback(self, interaction: discord.Interaction):
        if str(interaction.user.id) != str(self.user_id):
            embed = discord.Embed(title=f"You're not allowed to use this action!",
                                  description="",
                                  colour=discord.Color.red())
            return await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=2)

        world_id = self.values[0]

        exist_in_world = self.session.query(WorldHasUsers)\
            .filter(WorldHasUsers.user_id == self.user_id)\
            .filter(WorldHasUsers.world_id == world_id).first()

        if not exist_in_world:
            message = interaction.message
            edited_embed = message.embeds[0]
            edited_embed.colour = discord.Color.red()
            edited_embed.set_footer(text=f"You haven't joined this world anymore!")
            return await interaction.message.edit(embed=edited_embed, view=None)
        else:
            # remove world-user relation
            self.session.delete(exist_in_world)

            # remove player associated blocks
            upper_block = self.session.query(WorldHasBlocks).get(exist_in_world.upper_block_id)
            if upper_block:
                self.session.delete(upper_block)

            lower_block = self.session.query(WorldHasBlocks).get(exist_in_world.lower_block_id)
            if lower_block:
                self.session.delete(lower_block)

            self.session.commit()

            message = interaction.message
            edited_embed = message.embeds[0]
            edited_embed.colour = discord.Color.green()
            edited_embed.set_footer(text=f"Successfully removed world!")

            return await interaction.message.edit(embed=edited_embed, view=None)