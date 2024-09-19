import discord

from utils.jsonDataUtils import getData

async def success_embed(interaction, message: str = None, title: str = None, fields: list = None, thumbnail: str = None, image: str = None, channel: str = None, ephemeral: bool = False, view: discord.ui.View = None):
    if title:
        embed = discord.Embed(
            title=title,
            description=message,
            color=discord.Color.green()
        )
    else:
        embed = discord.Embed(
            title="",
            description=message,
            color=discord.Color.green()
        )

    if fields:
        for field in fields:
            embed.add_field(name=field[0], value=field[1], inline=field[2])

    if thumbnail:
        embed.set_thumbnail(url=thumbnail)

    if image:
        embed.set_image(url=image)

    if channel:
        channel_obj = interaction.guild.get_channel(channel)
        if channel_obj is None:
            raise ValueError(f"Channel with ID {channel} not found")
        await channel_obj.send(embed=embed, ephemeral=ephemeral, view=view)
    else:
        await interaction.response.send_message(embed=embed, ephemeral=ephemeral, view=view)

async def error_embed(interaction, message: str = None, title: str = None, fields: list = None, thumbnail: str = None, image: str = None, channel: int = None, ephemeral: bool = False, view: discord.ui.View = None):
    if title:
        embed = discord.Embed(
            title=title,
            description=message,
            color=discord.Color.red()
        )
    else:
        embed = discord.Embed(
            title="",
            description=message,
            color=discord.Color.red()
        )

    if fields:
        for field in fields:
            embed.add_field(name=field[0], value=field[1], inline=field[2])

    if thumbnail:
        embed.set_thumbnail(url=thumbnail)

    if image:
        embed.set_image(url=image)

    if channel:
        channel_obj = interaction.guild.get_channel(channel)
        if channel_obj is None:
            raise ValueError(f"Channel with ID {channel} not found")
        await channel_obj.send(embed=embed, ephemeral=ephemeral, view=view)
    else:
        await interaction.response.send_message(embed=embed, ephemeral=ephemeral, view=view)

async def color_embed(interaction, message: str = None, title: str = None, fields: list = None, thumbnail: str = None, image: str = None, channel: str = None, ephemeral: bool = False, view: discord.ui.View = None):
    user_id = str(interaction.user.id)
    color = getData('src/data/userData.json', user_id, 'preferred_color')
    if color is None:
        color = int('36393F', 16)
    else:
        color = int(color, 16)

    if title:
        embed = discord.Embed(
            title=title,
            description=message,
            color=color
        )
    else:
        embed = discord.Embed(
            title="",
            description=message,
            color=color
        )

    if fields:
        for field in fields:
            embed.add_field(name=field[0], value=field[1], inline=field[2])

    if thumbnail:
        embed.set_thumbnail(url=thumbnail)

    if image:
        embed.set_image(url=image)

    if channel:
        channel_obj = interaction.guild.get_channel(channel)
        if channel_obj is None:
            raise ValueError(f"Channel with ID {channel} not found")
        await channel_obj.send(embed=embed, ephemeral=ephemeral, view=view)
    else:
        await interaction.response.send_message(embed=embed, ephemeral=ephemeral, view=view)


# how to use:

"""
fields = {
    ('title 1', 'value 1', True),
    ('title 2', 'value 2', True)
}
# true/false determines if the field is inline or not

await success_embed(interaction,
    title='Title goes here',                    #(optional)
    message='Message',                          #(optional)
    fields=fields,                              #(optional)
    thumbnail='https://example.com/image.jpg'   #(optional)
    image='https://example.com/image.jpg'       #(optional)
    channel='channel_id',                       #(optional)
    view=your_view_instance                     #(optional)
    )
"""