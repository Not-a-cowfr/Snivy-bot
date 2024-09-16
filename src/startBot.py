from dotenv import load_dotenv


def main():
    import discord
    from discord.ext import commands
    from botSetup import bot

    from commands.commands import standalone_commands

    import os

    bot_token = os.getenv('BOT_TOKEN')

    @bot.event
    async def on_ready():
        print(f'Bot connected to Discord as {bot.user}')

        standalone_commands()

        try:
            # sync commands
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
    print('[WARNING] Tried calling startBot.py from another file!')