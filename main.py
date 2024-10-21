import asyncio
from discord_bot import discord_init
from web import send_message_to_chatgpt, driver_exit
from cmd import handle_command


async def main():
    discord_init()
    await asyncio.sleep(3)

    # 主循环，获取用户输入并发送给ChatGPT
    try:
        while True:
            user_input = await asyncio.to_thread(input, "请输入要发送的消息 (输入'q'退出): ")
            if user_input.lower() == 'q':
                break
            elif user_input.startswith('#'):
                # 如果输入以 # 开头，则处理指令
                await handle_command(user_input)
            else:
                await send_message_to_chatgpt(user_input)
    except Exception as e:
        print(f"出现错误: {e}")
    finally:
        driver_exit()


asyncio.run(main())
