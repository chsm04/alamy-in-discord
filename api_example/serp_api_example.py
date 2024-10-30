from serpapi import GoogleSearch

params = {
    "engine": "google",
    "q": "오늘",
    "api_key": ""
}

search = GoogleSearch(params)
results = search.get_dict()

for result in results['organic_results']:
    print(result['title'], result['link'])