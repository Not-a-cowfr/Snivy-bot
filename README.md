# Snivy Bot

Snivy Bot is a bot built for the hypixel guild "Snivy", all code is open source and the code is free to ~~steal~~ borrow, though I dont recommend using this poor code

## Features
- Report system
  - Report user via context menu
  - Report message via context menu
- Link command: `/link`
  - Unlink command: `/unlink`
- Uptime command: `/uptime`
- Xp leaderboard for a guild: `/guild xp`
- Uptime leaderboard for a guild: `/guild uptime`
- User role colors: `/color`
- Advanced bits comamnd: `/bits`
- Player tracking
  - Start tracking a player: `/track start` (limited to 10 players per person)
  - Stop tracking a player: `/track stop`
  - Stop tracking all players: `/track clear`
  - List all tracked players: `/track list`
- Misc context menu actions

and more to come...

## Bot Setup

1. Create a `.env` file in src, use the example provided for how to set it up
2. Install all dependencies (requests, discord, dotenv)
3. Run the bot and use the setup commands to set things up<br>
   3.1. Make sure you limit the setup/admin commands to be used by only admins
4. Enjoy the bot

## Setup commands
- Set the channel for reports to go to: `/setup report_channel`
- Set the Admin role for the server: `/setup admin_role`

## **FAQ:**

#### **Q:** Why are you using json files instead of a database?
**A:** I'm using json files because it's easier to manage and I don't need to worry about setting up a database, I will set up a database when the bot is fully fleshed out<br><br>

#### **Q:** When are you fixing your bot hosting?
**A:** Just like the reason why I'm using json files, i am hosting from my ide for quicker testing, I will use a hosting service whe the bot is done<br><br>

#### **Q:** Why is some of this code so ass?
**A:** This is just a side project for me, i am currently the only maintainer so the most important thing to me, is to have the code work<br><br>

## Self Promo 🙂
### `/g join Snivy`
### [Join the Discord!](https://discord.gg/Bu2KwE2U)
