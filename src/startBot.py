from src.commands.bits import update_ah_bits_item_prices


def main():
    import os

    from botSetup import bot
    from commands.commands import standalone_commands, Guild, Setup, Admin

    from tasks.bits import update_item_prices

    from src.utils.itemPriceUtils import get_ah_item_data


    bot_token = os.getenv('BOT_TOKEN')

    @bot.event
    async def on_ready():
        print(f'Bot connected to Discord as {bot.user}')

        bot.tree.add_command(Guild(name='guild'))
        bot.tree.add_command(Setup(name='setup'))
        bot.tree.add_command(Admin(name='admin'))
        standalone_commands()

        try:
            # sync commands to discord
            synced = await bot.tree.sync()
            print(f'Synced {len(synced)} command(s):')
            for command in synced:
                print(f'  /{command.name}')
        except Exception as e:
            print(f'Error syncing commands: {e}')

        #update_item_prices.start()
        #print(get_ah_item_data(['rock', '[Lvl 100] golden dragon']))

    @bot.event
    async def on_member_join(member):
        role_name = "unverified"
        guild = member.guild
        role = discord.utils.get(guild.roles, name=role_name)

        if role:
            await member.add_roles(role)
        else:
            print(f'Role: {role_name} not found')

    bot.run(bot_token)

if __name__ == '__main__':
    main()
else:
    print('>>> [WARNING] Tried calling startBot.py from another file!')