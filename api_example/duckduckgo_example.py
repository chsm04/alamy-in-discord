from duckduckgo_search import DDGS

ddgs = DDGS()


# DuckDuckGo 검색 함수 정의
def duckduckgo_search(query):
    results = ddgs.text(query, max_results=5)
    return results


print(duckduckgo_search("엘라스틱 서치"))