async def send_ranking():
    print("랭킹 전송 시작")

    sheet = gc.open("봄비길드 수로랭킹").sheet1
    data = sheet.get_all_values()

    # 👉 여기부터 ranking_text 시작
    ranking_text = ""

    # 🏆 TOP 3
    ranking_text += "🏆 **TOP 3**\n"
    for i in range(1, 4):
        rank = int(data[i][0])
        name = data[i][1]
        score = int(data[i][2])

        icons = ["🥇", "🥈", "🥉"]
        icon = icons[i-1]

        ranking_text += f"{icon} **{rank}위** │ `{name}`\n　　└ 💖 **{score:,}**\n\n"

    ranking_text += "━━━━━━━━━━━━━━━━━━\n\n"

    for i in range(4, 11):
        rank = int(data[i][0])
        name = data[i][1]
        score = int(data[i][2])

        ranking_text += f"🌸 {rank:>2}위 │ `{name}` │ {score:,}\n"

    ranking_text += "\n"

    for i in range(11, 21):
        rank = int(data[i][0])
        name = data[i][1]
        score = int(data[i][2])

        ranking_text += f"✨ {rank:>2}위 │ `{name}` │ {score:,}\n"

    embed = discord.Embed(
        title="🌸 봄비길드 수로 랭킹 🌸",
        description=ranking_text,
        color=0xffb6c1
    )

    channel = client.get_channel(CHANNEL_ID)
    await channel.send(embed=embed)