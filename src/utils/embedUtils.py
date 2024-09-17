import discord

from jsonDataUtils import getData

async def success_embed(interaction, message: str, title: str = None, fields: list = None, thumbnail: str = None):
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

    await interaction.response.send_message(embed=embed)

async def error_embed(interaction, message: str, title: str = None, fields: list = None, thumbnail: str = None):
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

    await interaction.response.send_message(embed=embed)

async def color_embed(interaction, message: str, title: str = None, fields: list = None, thumbnail: str = None):
    user_id = str(interaction.user.id)
    color = getData('src/userData.json', user_id, 'preferred_color')
    if color is None:
        color = int('36393F', 16)
    else:
        color = int(color, 16)

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

    await interaction.response.send_message(embed=embed)


# how to use:
"""
fields = {
    ('title 1', 'value 1', True),
    ('title 2', 'value 2', True)
}

# true/false determines if the field is inline or not

await success_embed(interaction,
    title='Title goes here (is optional)', #(optional)
    message='Message',
    fields=fields, #(optional)
    thumbnail='https://example.com/image.jpg' #(optional)
    )
"""

