import discord


async def edit_role(role: discord.Role, name: str, color: int):
    try:
        await role.edit(name=name, color=color)
        print(f"Role '{name}' edited successfully with color #{color:06x}.")
        return role
    except discord.DiscordException as e:
        print(f"Failed to edit role '{name}': {e}")
        return None


async def create_role(guild: discord.Guild, name: str, color: int):
    try:
        # checks if the role already exists, if it does, then it edits the role instead
        role_exists = discord.utils.get(guild.roles, name=name)
        if role_exists:
            return await edit_role(role_exists, name, color)

        role = await guild.create_role(name=name, color=discord.Color(color))
        print(f"Role '{name}' created successfully with color #{color:06x}.")
        return role
    except discord.DiscordException as e:
        print(f"Failed to create role '{name}': {e}")
        return None