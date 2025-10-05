elif choice == "3":
    bot_status["demo"] = False
    bot_status["telegram"] = False
    # also stop mini stats if running
    global MINI_STATS_RUNNING
    if MINI_STATS_RUNNING:
        MINI_STATS_RUNNING = False
        print("🛑 Mini Live Stats stopped automatically because bot was restarted.")
    time.sleep(1)
    bot_status["demo"] = True
    bot_status["telegram"] = True
    print("♻️ Demo bot restarted")
