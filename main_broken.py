
bash: syntax error near unexpected token `('
~/project_tb $             schedule_trade(symbol, direction, exec_time)bash: syntax error near unexpected token `symbol,'
~/project_tb $             print(f"📩 Received signal: {symbol} {direction}, scheduled in {TRADE_WAIT_SEC}s")
bash: syntax error near unexpected token `f"📩 Received signal: {symbol} {direction}, scheduled in {TRADE_WAIT_SEC}s"'
~/project_tb $
~/project_tb $     await client.run_until_disconnected()
bash: syntax error near unexpected token `('
~/project_tb $
~/project_tb $ # ---------- MAIN ----------
~/project_tb $ async def main():
bash: syntax error near unexpected token `('
~/project_tb $     bot_status = {"demo": True, "telegram": False}
No command bot_status found, did you mean:
 Command dot_static in package graphviz
~/project_tb $     print("🚀 Smart Trading Bot Running...")
bash: syntax error near unexpected token `"🚀 Smart Trading Bot Running..."'
~/project_tb $
~/project_tb $     for ch in channels:
>         print(f"📡 Listening to {ch}")
bash: syntax error near unexpected token `print'
~/project_tb $
~/project_tb $     # Start Telegram listener
~/project_tb $     asyncio.create_task(start_telegram(bot_status))
bash: syntax error near unexpected token `start_telegram'
~/project_tb $
~/project_tb $     # Start mini stats loop in separate thread
~/project_tb $     threading.Thread(target=mini_stats_loop, args=(bot_status,), daemon=True).start()
bash: syntax error near unexpected token `target=mini_stats_loop,'
~/project_tb $
~/project_tb $     # Keep main alive
~/project_tb $     while True:
>         await asyncio.sleep(1)
bash: syntax error near unexpected token `('
~/project_tb $
~/project_tb $ if __name__ == "__main__":
>     asyncio.run(main())
