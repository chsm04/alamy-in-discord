from openai_api import OpenAIChatClient  # 기존 openai_api 모듈
from bot import DiscordBotSingleton


# OpenAI API 클라이언트 초기화
open_ai_client = OpenAIChatClient()

# 싱글턴 인스턴스 가져오기
bot_instance = DiscordBotSingleton.get_instance()
# 명령어와 이벤트 등록
bot_instance.add_commands_and_events()
# 봇 실행
bot_instance.bot_run()