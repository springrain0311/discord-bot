async def send_ranking():
    print("🚀 랭킹 전송 시작")

    sheet = gc.open("봄비길드 수로랭킹")
    current_sheet = sheet.sheet1
    backup_sheet = sheet.get_worksheet(1)  # 두번째 시트

    current_data = current_sheet.get_all_values()
    old_data = backup_sheet.get_all_values()

    # 👉 이전 데이터 정리 (이름 → 순위)
    old_rank = {}
    for i in range(1, len(old_data)):
        name = old_data[i][1]
        rank = int(old_data[i][0])
        old_rank[name] = rank

    ranking_text = ""

    # 🏆 TOP 3
    ranking_text += "🏆 **TOP 3**\n"
    for i in range(1, 4):
        rank = int(current_data[i][0])
        name = current_data[i][1]
        score = int(current_data[i][2])

        icons = ["🥇", "🥈", "🥉"]
        icon = icons[i-1]

        # 🔺 변동 계산
        if name in old_rank:
            diff = old_rank[name] - rank
            if diff > 0:
                change = f" ▲{diff}"
            elif diff < 0:
                change = f" ▼{abs(diff)}"
            else:
                change = ""
        else:
            change = " NEW"

        ranking_text += f"{icon} **{rank}위** │ `{name}`{change}\n　　└ 💖 **{score:,}**\n\n"

    ranking_text += "━━━━━━━━━━━━━━━━━━\n\n"

    # 🌸 4~10위
    for i in range(4, 11):
        rank = int(current_data[i][0])
        name = current_data[i][1]
        score = int(current_data[i][2])

        if name in old_rank:
            diff = old_rank[name] - rank
            if diff > 0:
                change = f" ▲{diff}"
            elif diff < 0:
                change = f" ▼{abs(diff)}"
            else:
                change = ""
        else:
            change = " NEW"

        ranking_text += f"🌸 {rank:>2}위 │ `{name}`{change} │ {score:,}\n"

    ranking_text += "\n"

    # ✨ 11~20위
    for i in range(11, 21):
        rank = int(current_data[i][0])
        name = current_data[i][1]
        score = int(current_data[i][2])

        if name in old_rank:
            diff = old_rank[name] - rank
            if diff > 0:
                change = f" ▲{diff}"
            elif diff < 0:
                change = f" ▼{abs(diff)}"
            else:
                change = ""
        else:
            change = " NEW"

        ranking_text += f"✨ {rank:>2}위 │ `{name}`{change} │ {score:,}\n"

    embed = discord.Embed(
        title="🌸 봄비길드 수로 랭킹 🌸",
        description=ranking_text,
        color=0xffb6c1
    )

    channel = client.get_channel(CHANNEL_ID)
    await channel.send(embed=embed)

    print("✅ 메시지 전송 완료")

    # 🔥 현재 데이터를 백업 시트에 저장 (다음주 비교용)
    backup_sheet.clear()
    backup_sheet.update(current_data)

    print("📦 이전 데이터 저장 완료")