import faiss
import numpy as np
from datetime import datetime
from openai import OpenAI

client = OpenAI()

class ConversationHistory:
    def __init__(self, embedding_dim=1536):
        self.embedding_dim = embedding_dim
        self.index = faiss.IndexFlatL2(self.embedding_dim)
        self.messages = []  # 메시지와 메타 데이터 함께 저장

    def get_embedding(self, text):
        response = client.embeddings.create(
            input=text,
            model="text-embedding-3-small"
        )
        return np.array(response.data[0].embedding, dtype=np.float32)

    def add_message(self, uid, conversation_id, role, content):
        embedding = self.get_embedding(content)
        timestamp = datetime.now().isoformat()  # 타임스탬프 추가
        self.messages.append({
            "uid": uid,
            "conversation_id": conversation_id,
            "role": role,
            "content": content,
            "timestamp": timestamp
        })
        self.index.add(np.array([embedding]))

    def search_messages(self, query, uid=None, start_date=None, end_date=None, limit=5):
        """
        query (str): 검색할 쿼리
        uid (str, optional): 검색할 사용자 ID. 기본값은 None으로 모든 사용자 대상.
        start_date (str, optional): 검색 시작 날짜. ISO 형식 (예: "2023-10-25").
        end_date (str, optional): 검색 종료 날짜. ISO 형식 (예: "2023-10-26").
        limit (int): 반환할 유사 메시지 수 (기본값: 5)
        """
        query_embedding = self.get_embedding(query).reshape(1, -1)
        distances, indices = self.index.search(query_embedding, limit)

        # 검색 조건에 따른 필터링
        filtered_messages = []
        for idx in indices[0]:
            msg = self.messages[idx]
            # UID 조건 검사
            if uid and msg["uid"] != uid:
                continue
            # 날짜 조건 검사
            if start_date or end_date:
                msg_date = datetime.fromisoformat(msg["timestamp"]).date()
                if start_date and msg_date < datetime.fromisoformat(start_date).date():
                    continue
                if end_date and msg_date > datetime.fromisoformat(end_date).date():
                    continue
            filtered_messages.append(msg)
        
        # 타임스탬프 기준 정렬 후 제한 적용
        filtered_messages = sorted(filtered_messages, key=lambda x: x["timestamp"], reverse=True)
        return filtered_messages[:limit]

# 예제 사용
if __name__ == "__main__":
    conv_history = ConversationHistory()
    conv_history.add_message("user123", "conv1", "user", "오늘 점심 뭐 먹을까?")
    conv_history.add_message("user123", "conv1", "assistant", "오늘 날씨가 좋으니 밖에서 먹는 건 어때요?")
    conv_history.add_message("user456", "conv2", "user", "오늘 저녁에 뭐하지?")
    
    # 특정 사용자의 대화만 검색
    result = conv_history.search_messages("내가 뭐라했지", uid="user123")
    print("특정 사용자 대화 검색 결과:", result)

    # 날짜 범위를 지정한 검색 예시
    result = conv_history.search_messages("내가 뭐라했지", start_date="2023-10-25", end_date="2023-10-26")
    print("날짜 범위 대화 검색 결과:", result)

    # 모든 사용자와 전체 기간을 대상으로 검색
    result = conv_history.search_messages("내가 뭐라했지")
    print("모든 사용자 전체 기간 검색 결과:", result)