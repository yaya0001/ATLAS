import json

from app.tools import tool_executor

result = tool_executor.execute(
    name="web_search",
    arguments={
        "query": "Latest developments in Agentic AI 2026",
        "max_results": 3,
    },
)

results = json.loads(result)

for item in results:
    print(f"Title: {item['title']}")
    print(f"URL: {item['url']}")
    print(f"Content: {item['content'][:200]}")
    print("-" * 50)