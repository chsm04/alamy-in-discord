import asyncio
from openai_api import OpenAIChatClient

openai_client = OpenAIChatClient()

# 토큰 분할 함수 (토큰을 띄어쓰기 기준으로 분리하는 간단한 예)
def count_tokens(text):
    return len(text.split())

# OpenAI API 스트리밍 응답을 처리하는 함수
async def stream_openai_response(channel, prompt_message, response_message,token_threshold=40):
    full_response = ""  # 전체 응답을 저장할 변수
    token_count = 0  # 누적된 토큰 수
    
    try:
        # OpenAI API에서 스트림으로 응답 받기
        async for delta in openai_client.stream_chat_completion([{"role": "user", "content": prompt_message}]):
            full_response += delta  # 응답 누적
            token_count += count_tokens(delta)  # 새로운 토큰 개수 누적

            # 토큰이 설정한 기준만큼 쌓였을 때만 메시지 수정
            if token_count >= token_threshold:
                await response_message.edit(content=full_response)
                token_count = 0  # 기준에 도달하면 토큰 수 초기화
                await asyncio.sleep(0.5)  # 0.5초 대기

        # 스트림이 끝나면 최종 응답을 수정
        await response_message.edit(content=full_response)

    except Exception as e:
        await channel.send(f"Error: {str(e)}")