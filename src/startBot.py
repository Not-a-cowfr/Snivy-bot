from dotenv import load_dotenv

def main():
    import discord
    from discord.ext import commands
    from botSetup import bot, api_key

    from commands.commands import standalone_commands, Guild, Setup
    from utils.serverManagement import isInGuild

    import os

    bot_token = os.getenv('BOT_TOKEN')

    @bot.event
    async def on_ready():
        print(f'Bot connected to Discord as {bot.user}')

        bot.tree.add_command(Guild(name='guild'))
        bot.tree.add_command(Setup(name='setup'))
        standalone_commands()

        start_guild_checks = isInGuild(api_key)
        start_guild_checks.start(bot.guilds[0])

        try:
            # sync commands to discord
            synced = await bot.tree.sync()
            print(f'Synced {len(synced)} command(s):')
            for command in synced:
                print(f'  /{command.name}')
        except Exception as e:
            print(f'Error syncing commands: {e}')

    bot.run(bot_token)

if __name__ == '__main__':
    main()
else:
    print('>>> [WARNING] Tried calling startBot.py from another file!')