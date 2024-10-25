from dotenv import load_dotenv
from nextcord.ext import commands
import nextcord
import os
from util import *

class DiscordBotSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DiscordBotSingleton, cls).__new__(cls)
            load_dotenv()
            cls._instance.DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

            # 디스코드 봇 설정
            intents = nextcord.Intents.default()
            intents.message_content = True  # 메시지 콘텐츠 접근 허용
            cls._instance.bot = commands.Bot(command_prefix="$", intents=intents)
        return cls._instance

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def bot_run(self):
        self.bot.run(self.DISCORD_TOKEN)

    def add_commands_and_events(self):
        @self.bot.command(name="ask")
        async def ask_openai(ctx, *, question):
            # 응답을 받을 기본 메시지 생성
            response_message = await ctx.send("생각중...")
            
            # OpenAI API 스트리밍 응답 처리
            await stream_openai_response(ctx.channel, question, response_message)

        @self.bot.event
        async def on_message(message):
            if message.author == self.bot.user:
                return

            # 특정 단어가 포함된 메시지 감지
            if "안녕" in message.content:
                await message.channel.send("안녕하세요! 👋")
            elif "$" in message.content:
                return
            else:
                response_message = await message.channel.send("생각중...")
                await stream_openai_response(message.channel, message.content, response_message)

            await self.bot.process_commands(message)


