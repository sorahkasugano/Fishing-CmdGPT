import asyncio
import time

import discord
import aiohttp
from conf import config

# 创建 Discord 客户端
intents = discord.Intents.default()
intents.messages = True


# 自定义 Discord 客户端
class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.channel = None  # 将 channel 作为类的实例属性

    async def on_ready(self):
        print(f'已登录到 Discord 为 {self.user}')
        self.channel = client.get_channel(config["CHANNEL_ID"])
        if self.channel:
            print(f'已连接到频道: {self.channel}')
        else:
            print("无法找到指定的频道")

    # 启动事件循环并发送消息到 Discord
    async def send_message_to_discord(self, last_turn_text):
        if self.channel:
            # 发送消息到指定频道
            # Discord 消息长度限制为 2000 字符, 语音播报限制 250 字符
            max_message_length = 250

            if len(last_turn_text) > max_message_length:
                # 分割消息并逐条发送
                for i in range(0, len(last_turn_text), max_message_length):
                    # 按 250 字符为一段切割字符串并发送
                    await self.channel.send(f'{last_turn_text[i:i + max_message_length]}')
                    await asyncio.sleep(70)
            else:
                # 如果消息未超过 250 字符，直接发送
                await self.channel.send(f'{last_turn_text}')
            print("消息已发送")

    async def run_client_in_background(self):
        """后台运行 Discord 客户端"""
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector()) as session:
            self.http._session = session
            self.http.proxy = config["PROXY_URL"]  # 设置代理
            await self.start(config["DISCORD_TOKEN"])  # 阻塞在 start() 内部


client = MyClient(intents=intents)
