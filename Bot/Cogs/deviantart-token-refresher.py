import asyncio
import datetime
import os
import time

import requests
import ujson
from discord.ext import commands, tasks
from dotenv import load_dotenv

load_dotenv()

Refresh_Token = os.getenv("DeviantArt_Refresh_Token")
Client_ID = os.getenv("DeviantArt_Client_ID")
Client_Secret = os.getenv("DeviantArt_Client_Secret")


class tokenRefresher(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.index = 0
        self.refresher.start()

    @tasks.loop(minutes=45.0)
    async def refresher(self):
        self.index = self.index + 1
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
        link = f"https://www.deviantart.com/oauth2/token?client_id={Client_ID}&client_secret={Client_Secret}&grant_type=refresh_token&refresh_token={Refresh_Token}"
        await asyncio.sleep(10)
        r = requests.get(link)
        data = ujson.loads(r.text)
        access_token = data["access_token"]
        refresh_token = data["refresh_token"]
        print(
            f"----------DeviantArt Token Refresher - Request #{self.index} - {st}-----------------\n"
        )
        print(f"{data}\n")
        print(f"New DeviantArt Access Token: {access_token}\n")
        print(f"New DeviantArt Refresh Token: {refresh_token}\n")
        print(
            "----------------------------------------------------------------------------\n"
        )
        with open("../.env", "r") as file:
            file_data = file.readlines()
            file_data[37] = f'DeviantArt_Access_Token = "{access_token}"\n'
            file_data[38] = f'DeviantArt_Refresh_Token = "{refresh_token}"\n'
        with open("../.env", "w") as file:
            file.writelines(file_data)


def setup(bot):
    bot.add_cog(tokenRefresher(bot))
