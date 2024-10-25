import os
from openai import OpenAI

class OpenAIChatClient:
    _instance = None
    history = []

    def __new__(cls, *args, **kwargs):
        """
        싱글턴 패턴 적용을 위한 __new__ 메서드.
        클래스 인스턴스가 이미 존재하면 기존 인스턴스를 반환.
        """
        if cls._instance is None:
            cls._instance = super(OpenAIChatClient, cls).__new__(cls)
        return cls._instance

    def __init__(self, api_key=None, model="gpt-4"):
        """
        OpenAIChatClient 클래스 초기화. API 키를 받아 OpenAI 클라이언트를 설정.
        기본적으로 환경 변수에서 API 키를 가져오며, 필요시 매개변수로 직접 전달 가능.

        Args:
            api_key (str): OpenAI API 키 (기본값: 환경 변수 "OPENAI_API_KEY"에서 가져옴)
            model (str): 사용할 모델 (기본값: "gpt-4")
        """
        # 이미 초기화된 인스턴스라면 다시 초기화하지 않도록 처리
        if not hasattr(self, "initialized"):
            self.api_key = api_key or os.getenv("OPENAI_API_KEY")
            if not self.api_key:
                raise ValueError("API 키가 제공되지 않았습니다. 환경 변수 또는 매개변수로 API 키를 설정하세요.")
            self.client = OpenAI(api_key=self.api_key)
            self.model = model
            self.initialized = True  # 초기화가 완료된 인스턴스라는 플래그 설정

    async def stream_chat_completion(self, messages):
        """
        OpenAI API의 스트리밍 응답을 처리하는 함수.

        Args:
            messages (list): 역할과 내용이 포함된 메시지 리스트. 예: [{"role": "user", "content": "Say this is a test"}]

        Yields:
            str: 스트리밍 방식으로 받은 텍스트 델타.
        """
        try:
            # 스트리밍 방식으로 채팅 응답 생성
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                stream=True
            )
            
            # 스트림으로 받은 델타를 실시간으로 처리
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    print(chunk.choices[0].delta.content)
                    yield chunk.choices[0].delta.content
        except Exception as e:
            yield f"Error: {str(e)}"