from system_client_singleton import SystemClientSingleton


system = SystemClientSingleton()

# OpenAI API 클라이언트 초기화
open_ai_client = system.get_openai_client()

# 싱글턴 인스턴스 가져오기
bot_instance = system.get_discord_bot()
# 명령어와 이벤트 등록
bot_instance.add_commands_and_events()
# 봇 실행
bot_instance.bot_run()