from dotenv import load_dotenv
import os
from openai_api import OpenAIChatClient
from conversation_history import ConversationHistory 
from bot import DiscordClient

class SystemClientSingleton:
    _instance = None
    _discord_client = None
    _openai_client = None
    _history_manager = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SystemClientSingleton, cls).__new__(cls)
            load_dotenv()  # 환경 변수 로드
        return cls._instance

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def get_discord_bot(self):
        """
        싱글톤 Discord 봇 인스턴스를 반환합니다.
        봇이 없으면 새로 생성하고, 있으면 기존 봇을 반환합니다.
        """
        if self._discord_client is None:
            self._discord_client = DiscordClient()

        return self._discord_client

    def get_openai_client(self):
        """
        싱글톤 OpenAI 클라이언트 인스턴스를 반환합니다.
        클라이언트가 없으면 새로 생성하고, 있으면 기존 클라이언트를 반환합니다.
        """
        if self._openai_client is None:
            self._openai_client = OpenAIChatClient()
            
        return self._openai_client


    def get_history_manager(self):
        """
        싱글톤 히스토리 매니저 인스턴스를 반환합니다.
        매니저가 없으면 새로 생성하고, 있으면 기존 매니저를 반환합니다.
        """
        if self._history_manager is None:
            self._history_manager = ConversationHistory()
            
        return self._history_manager


# # 사용 예시
# if __name__ == "__main__":
#     # SystemClientSingleton 인스턴스 생성 및 Discord, OpenAI 클라이언트 가져오기
#     system_client = SystemClientSingleton.get_instance()
#     discord_bot = system_client.get_discord_bot()
#     openai_client = system_client.get_openai_client()
    
#     print(f"Discord Bot ID: {discord_bot.user.id if discord_bot.user else 'None'}")
#     print(f"OpenAI Client API Key 존재 여부: {'Yes' if openai_client else 'No'}")