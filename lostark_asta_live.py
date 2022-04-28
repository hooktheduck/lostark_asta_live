import dotenv
import requests
import os
import discord

from dotenv import load_dotenv
from discord.ext import commands, tasks

dotenv_file = dotenv.find_dotenv()
load_dotenv(dotenv_file)
discordBotToken = os.getenv("DISCORD_BOT_TOKEN")
discordName = os.getenv("DISCORD_NAME")
channelId = os.getenv("CHANNEL_ID")
bot = commands.Bot(command_prefix='!')


def getAstaStatus():
    response = requests.get("https://lost-ark-api.vercel.app/server/all").json()['data']['Asta'].split(" ")[1]

    if response == "Maintenance" or response == "Offline":
        return "Offline"

    if response == "Full" or response == "Busy" or response == "Online" or response == "Good":
        return "Online"


async def update():
    if os.getenv("astaStatus") != getAstaStatus():
        if os.getenv("astaStatus") == 'Offline' and getAstaStatus() == "Online":
            channel = bot.get_channel(channelId)
            await channel.send("Der Server **Asta** ist wieder online!")
            print("Server wieder online!")
            dotenv.set_key(dotenv_file, "astaStatus", getAstaStatus())

        if os.getenv("astaStatus") == "Online" and getAstaStatus() == 'Offline':
            channel = bot.get_channel(channelId)
            await channel.send("Der Server **Asta** ist jetzt offline!")
            print("Server ist offline!")
            dotenv.set_key(dotenv_file, "astaStatus", getAstaStatus())


@bot.event
async def on_ready():
    dotenv.set_key(dotenv_file, "astaStatus", getAstaStatus())
    await updateTimer.start()


@tasks.loop(seconds=int(60))
async def updateTimer(status):
    await update()


bot.run(discordBotToken)



