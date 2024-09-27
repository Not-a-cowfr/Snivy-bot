import discord
from discord.errors import NotFound

from utils.jsonDataUtils import getData


async def success_embed(
        interaction=None,  # required
        message: str = None,  # required
        title: str = None,
        fields: list = None,
        thumbnail: str = None,
        image: str = None,
        channel: int = None,
        ephemeral: bool = False,
        view: discord.ui.View = None,
):
    if interaction is None:
        print("Someones stupid ass forgot to add interaction to a `color_embed` call")
        return None

    if message is None:
        await error_embed(interaction, message="Error: no message was provided for embed creation")

    embed = discord.Embed(
        title=title, description=message, color=discord.Color.green()
    )

    if fields:  # if there are any info fields then it adds them to the embed
        for field in fields:
            embed.add_field(name=field[0], value=field[1], inline=field[2])

    # TODO validate if thumbnail is a valid URL
    if thumbnail:  # if there is a thumbnail then it adds it to the embed
        embed.set_thumbnail(url=thumbnail)

    # TODO validate if image is a valid URL
    if image:  # if there is an image then it adds it to the embed
        embed.set_image(url=image)

    channel_obj = None
    if channel:  # if a channel is specified then it sends the embed to that channel
        channel_obj = interaction.guild.get_channel(channel)
        if channel_obj is None:
            raise ValueError(f'Channel with ID {channel} not found')

    # if a view (like buttons and dropdowns) are included then it sends the embed with the view, along with the checks for if channel is specified
    if view:
        if channel_obj:
            await channel_obj.send(embed=embed, ephemeral=ephemeral, view=view)
        else:
            await interaction.followup.send(embed=embed, ephemeral=ephemeral, view=view)
    else:
        if channel_obj:
            await channel_obj.send(embed=embed, ephemeral=ephemeral)
        else:
            await interaction.followup.send(embed=embed, ephemeral=ephemeral)


async def error_embed(
    interaction = None, # required
    message: str = None, # required
    title: str = None,
    fields: list = None,
    thumbnail: str = None,
    image: str = None,
    channel: int = None,
    ephemeral: bool = False,
    view: discord.ui.View = None,
):
    if interaction is None:
        print("Someones stupid ass forgot to add interaction to a `color_embed` call")
        return None

    if message is None:
        await error_embed(interaction, message="Error: no message was provided for embed creation")

    embed = discord.Embed(
        title=title, description=message, color=discord.Color.red()
    )

    if fields:  # if there are any info fields then it adds them to the embed
        for field in fields:
            embed.add_field(name=field[0], value=field[1], inline=field[2])

    # TODO validate if thumbnail is a valid URL
    if thumbnail:  # if there is a thumbnail then it adds it to the embed
        embed.set_thumbnail(url=thumbnail)

    # TODO validate if image is a valid URL
    if image:  # if there is an image then it adds it to the embed
        embed.set_image(url=image)

    channel_obj = None
    if channel:  # if a channel is specified then it sends the embed to that channel
        channel_obj = interaction.guild.get_channel(channel)
        if channel_obj is None:
            raise ValueError(f'Channel with ID {channel} not found')

    # if a view (like buttons and dropdowns) are included then it sends the embed with the view, along with the checks for if channel is specified
    if view:
        if channel_obj:
            await channel_obj.send(embed=embed, ephemeral=ephemeral, view=view)
        else:
            await interaction.followup.send(embed=embed, ephemeral=ephemeral, view=view)
    else:
        if channel_obj:
            await channel_obj.send(embed=embed, ephemeral=ephemeral)
        else:
            await interaction.followup.send(embed=embed, ephemeral=ephemeral)


async def color_embed(
    interaction = None, # required
    message: str = None, # required
    title: str = None,
    fields: list = None,
    thumbnail: str = None,
    image: str = None,
    channel: str = None,
    ephemeral: bool = False,
    view: discord.ui.View = None,
):
    if interaction is None:
        print("Someones stupid ass forgot to add interaction to a `color_embed` call")
        return None

    if message is None:
        await error_embed(interaction, message="Error: no message was provided for embed creation")

    user_id = str(interaction.user.id) # get user id of the person who interacted

    color = getData('src/data/userData.json', user_id, 'preferred_color') # gets the preferred color of the user
    if color is None:
        color = int('36393F', 16) # if no preferred color is found then it defaults to like a grayish color
    else:
        color = int(color, 16) # if a preferred color is found then it converts it from hex to the format that works for discord

    embed = discord.Embed(
        title=title, description=message, color=color
    )

    if fields:  # if there are any info fields then it adds them to the embed
        for field in fields:
            embed.add_field(name=field[0], value=field[1], inline=field[2])

    # TODO validate if thumbnail is a valid URL
    if thumbnail:  # if there is a thumbnail then it adds it to the embed
        embed.set_thumbnail(url=thumbnail)

    # TODO validate if image is a valid URL
    if image:  # if there is an image then it adds it to the embed
        embed.set_image(url=image)

    channel_obj = None
    if channel:  # if a channel is specified then it sends the embed to that channel
        channel_obj = interaction.guild.get_channel(channel)
        if channel_obj is None:
            raise ValueError(f'Channel with ID {channel} not found')

    # if a view (like buttons and dropdowns) are included then it sends the embed with the view, along with the checks for if channel is specified
    if view:
        if channel_obj:
            await channel_obj.send(embed=embed, ephemeral=ephemeral, view=view)
        else:
            await interaction.followup.send(embed=embed, ephemeral=ephemeral, view=view)
    else:
        if channel_obj:
            await channel_obj.send(embed=embed, ephemeral=ephemeral)
        else:
            await interaction.followup.send(embed=embed, ephemeral=ephemeral)


# how to use:

"""
fields = {
    ('title 1', 'value 1', True),
    ('title 2', 'value 2', True)
}
"""
# true/false determines if the field is inline or not

"""
await success_embed(interaction,
    title='Title goes here', 
    message='Message', 
    fields=fields, 
    thumbnail='https://example.com/image.jpg'
    image='https://example.com/image.jpg'
    channel='channel_id',
    view=your_view_instance
    )
"""
# all params are optional besides interaction, no clue why you would want to call this without any message, but you can
