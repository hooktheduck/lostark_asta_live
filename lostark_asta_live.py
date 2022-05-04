import dotenv
import requests
import os
import discord
import pickle 
import lostark_server_api as api

from dotenv import load_dotenv
from discord.ext import commands, tasks

dotenv_file = dotenv.find_dotenv()
load_dotenv(dotenv_file)
discordBotToken = os.getenv("DISCORD_BOT_TOKEN")
discordName = os.getenv("DISCORD_NAME")
channelId = os.getenv("CHANNEL_ID")
bot = commands.Bot(command_prefix='!')


def load():
    with open('data.txt') as f:
        return f.read()

def write(text):
    with open("data.txt", "w") as text_file:
        text_file.write(text)

def getAstaStatus():

    try:
        check = requests.get("https://lastarkapi-m2.herokuapp.com/server/all").json()['data']
    except:
        check = requests.get("https://lost-ark-api.vercel.app/server/all").json()['data'] 

    if not check:
        return "Offline" 

    # Namen für Offline-Status
    offlineList = ["Maintenance", "Offline"]

    # Namen für Online-Status
    onlineList = ["Full", "Busy", "Online", "Good", "Ok"]

    try:
        response = api.getStatusOf("Asta")
    except:
        try:
            response = requests.get("https://lastarkapi-m2.herokuapp.com/server/all").json()['data']['Asta'].split(" ")[1]
        except:
            response = requests.get("https://lost-ark-api.vercel.app/server/all").json()['data']['Asta'].split(" ")[1]
    
    if response in offlineList:
        return "Offline"

    if response in onlineList:
        return "Online"


async def update():
    if load() != getAstaStatus():
        if load() == 'Offline' and getAstaStatus() == "Online":
            channel = bot.get_channel(int(channelId))
            await channel.send("Der Server **Asta** ist wieder online!")
            print("Server wieder online!")
            write(getAstaStatus())

        if load() == "Online" and getAstaStatus() == 'Offline':
            channel = bot.get_channel(int(channelId))
            await channel.send("Der Server **Asta** ist jetzt offline!")
            print("Server ist offline!")
            write(getAstaStatus())


@bot.event
async def on_ready():
    try:
        write(getAstaStatus())
    except Exception as e:
        print(e)
        
    await updateTimer.start()



@tasks.loop(seconds=int(60))
async def updateTimer():
    print("Updated [every 60s]")
    try:
        await update()
    except Exception as e:
        print(e)

bot.run(discordBotToken)




