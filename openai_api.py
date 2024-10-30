import os
from openai import OpenAI
from dto.message_dto import MessageDTO
import asyncio

class OpenAIChatClient:

    def __init__(self, api_key=None, model="gpt-4"):
        from system_client_singleton import SystemClientSingleton
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.system = SystemClientSingleton().get_instance()
        if not self.api_key:
            raise ValueError("API 키가 제공되지 않았습니다. 환경 변수 또는 매개변수로 API 키를 설정하세요.")
        self.client = OpenAI(api_key=self.api_key)
        self.model = model
        self.history_manager = self.system.get_history_manager() # ConversationHistory 인스턴스 생성
        self.initialized = True
        self.discord_client = self.system.get_discord_bot()
            

    async def stream_chat_completion(self, message_object: MessageDTO):
        """
        OpenAI API의 스트리밍 응답을 처리하는 함수.

        Args:
            conversation_id (str): 대화의 고유 ID
            message (dict): 역할과 내용이 포함된 단일 메시지. 예: {"role": "user", "content": "Say this is a test"}

        Yields:
            str: 스트리밍 방식으로 받은 텍스트 델타.
        """
        try:
            # 사용자 메시지 저장
            self.history_manager.add_message(
                uid=message_object.uid,
                conversation_id=self.history_manager.generate_conversation_id(uid=message_object.uid),
                role="user",
                content=message_object.content
            )


            # 스트리밍 방식으로 채팅 응답 생성
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role" : "user","content" : message_object.content}],
                temperature=0.7,
                stream=True
            )

            # 전체 응답을 모아 하나의 메시지로 저장하기 위한 변수
            full_response = ""

            # 스트림으로 받은 델타를 실시간으로 처리
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    full_response += content  # 응답을 계속 이어붙이기
                    yield content  # 실시간 스트리밍으로 전송
                    await asyncio.sleep(0)  # 비동기적으로 처리하도록 기다림

            # 완성된 응답 메시지를 ConversationHistory에 저장
            self.history_manager.add_message(
                uid="assistant",
                conversation_id=self.history_manager.generate_conversation_id(uid=self.discord_client.get_bot_id),
                role="assistant",
                content=full_response
            )
            
        except Exception as e:
            yield f"Error: {str(e)}"

# conversation_history.py 내용 예시 (ConversationHistory 클래스)
# ConversationHistory 클래스는 "uid", "conversation_id", "role", "content" 필드가 포함된 메시지를 저장하는 역할을 함