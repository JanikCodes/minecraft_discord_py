import json

import discord

import db


class ClassSelectButton(discord.ui.Button):
    def __init__(self, text, user, last_page, data):
        super().__init__(label=text, style=discord.ButtonStyle.primary, disabled=False)
        self.user = user
        self.last_page = last_page
        self.data = data

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.user.id:
            embed = discord.Embed(title=f"You're not allowed to use this action!",
                                  description="",
                                  colour=discord.Color.red())
            return await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=2)

        await interaction.response.defer()

        # check if user already has a class, just in case
        if not db.validate_user(self.user.id):
            # add user now to database
            db.add_user(self.user.id, self.user.name)

            # update attributes according to selected class
            for stat_name, stat_value in self.data[self.last_page]['stats'].items():
                db.set_stat_from_user_with_id(self.user.id, stat_name, stat_value)

            for eq_name, eq_value in self.data[self.last_page]['equip'].items():
                if eq_value:
                    item = db.add_item_to_user_with_item_name(idUser=self.user.id, item_name=eq_value)
                    db.equip_item(idUser=self.user.id, item=item)

            # update embed to inform player of the success.
            class_name = self.data[self.last_page]['name'].replace("'", "''")
            message = interaction.message
            edited_embed = message.embeds[0]
            edited_embed.colour = discord.Color.green()
            edited_embed.add_field(name=f"Success!", value=f"You've selected the class **{class_name}**!", inline=False)

            await interaction.message.edit(embed=edited_embed, view=None, delete_after=2)
        else:
            message = interaction.message
            edited_embed = message.embeds[0]
            edited_embed.colour = discord.Color.red()
            edited_embed.add_field(name=f"Failure!", value=f"You've already selected a class..", inline=False)

            await interaction.message.edit(embed=edited_embed, view=None, delete_after=2)


class ClassSelectionPageButton(discord.ui.Button):
    def __init__(self, text, direction, user, last_page, data):
        super().__init__(label=text, style=discord.ButtonStyle.secondary, disabled=False)
        self.direction = direction
        self.user = user
        self.last_page = last_page
        self.data = data

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.user.id:
            embed = discord.Embed(title=f"You're not allowed to use this action!",
                                  description="",
                                  colour=discord.Color.red())
            return await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=2)

        await interaction.response.defer()

        if self.direction == 'next':
            new_index = 0 if self.last_page + 1 > (len(self.data) - 1) else self.last_page + 1
            await view_class_selection_page(interaction=interaction, data=self.data, index=new_index)
        elif self.direction == 'prev':
            new_index = (len(self.data) - 1) if self.last_page - 1 < 0 else self.last_page - 1
            await view_class_selection_page(interaction=interaction, data=self.data, index=new_index)


class ClassSelectionView(discord.ui.View):
    def __init__(self, user, current_page, data):
        super().__init__()
        class_name = data[current_page]['name'].replace("'", "''")
        self.user = user
        self.add_item(
            ClassSelectionPageButton(text="Previous", direction="prev", user=user, last_page=current_page, data=data))
        self.add_item(
            ClassSelectionPageButton(text="Next", direction="next", user=user, last_page=current_page, data=data))
        self.add_item(ClassSelectButton(text=f"Select {class_name}", user=user, last_page=current_page, data=data))


async def class_selection(interaction: discord.Interaction):
    # read the JSON file
    with open('Data/classes.json', 'r') as f:
        data = json.load(f)

    if interaction.user.id != 321649314382348288:
        data.pop(-1)  # remove god class

    await view_class_selection_page(interaction=interaction, data=data, index=0)


async def view_class_selection_page(interaction, data, index):
    embed = discord.Embed(title=f"Welcome {interaction.user.name}! *please choose your start class!*",
                          description=f"")
    # iterate over the objects
    ed_class = data[index]

    class_name = ed_class['name'].replace("'", "''")
    class_desc = ed_class['description'].replace("'", "''")
    class_img_url = ed_class['image']

    embed.add_field(name=f"**{class_name}**", value=class_desc, inline=False)

    stat_text = str()
    eq_text = str()
    # add all the class stats
    for stat_name, stat_value in ed_class['stats'].items():
        stat_text += f"**{stat_name[:3].capitalize()}**: `{stat_value}` "

    for eq_name, eq_value in ed_class['equip'].items():
        if eq_name == "weapon":
            eq_text += f"**Weapon**: `{eq_value}` \n **Armor**: "
        else:
            if eq_value:
                eq_text += f" `{eq_value}` "

    embed.add_field(name="Statistics:", value=stat_text, inline=False)
    embed.add_field(name="Equipment:", value=eq_text, inline=False)

    embed.set_thumbnail(url=class_img_url)

    if interaction.message:
        await interaction.message.edit(embed=embed,
                                       view=ClassSelectionView(user=interaction.user, current_page=index, data=data))
    else:
        await interaction.response.send_message(embed=embed,
                                                view=ClassSelectionView(user=interaction.user, current_page=index,
                                                                        data=data))
