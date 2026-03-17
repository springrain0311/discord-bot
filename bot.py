import discord
import gspread
import os
import asyncio
from oauth2client.service_account import ServiceAccountCredentials

TOKEN = os.environ.get("DISCORD_TOKEN")
CHANNEL_ID = int(os.environ.get("CHANNEL_ID"))

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "service_account.json", scope
)
gc = gspread.authorize(creds)

intents = discord.Intents.default()
client = discord.Client(intents=intents)


async def send_ranking():
    print("랭킹 전송 시작")

    sheet = gc.open("봄비길드 수로랭킹").sheet1
    data = sheet.get_all_values()

    print("데이터 길이:", len(data))

    ranking_text = ""

    for i in range(1, 21):
        rank = int(data[i][0])
        name = data[i][1]
        score = data[i][2]

        if rank == 1:
            icon = "🥇"
        elif rank == 2:
            icon = "🥈"
        elif rank == 3:
            icon = "🥉"
        elif 4 <= rank <= 10:
            icon = "🌸"
        else:
            icon = "✨"

        ranking_text += f"{icon} {rank}위 {name} │ {score}\n"

    embed = discord.Embed(
        title="🌸 봄비길드 수로 랭킹 TOP20 🌸",
        description=ranking_text,
        color=0xff99cc
    )

    channel = await client.fetch_channel(CHANNEL_ID)  # 🔥 이거로 변경
    print("채널 fetch:", channel)

    await channel.send(embed=embed)


@client.event
async def on_ready():
    print(f"로그인됨: {client.user}")

    channel = client.get_channel(CHANNEL_ID)
    print("채널:", channel)

    await send_ranking()
    await client.close()


async def main():
    await client.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(main())