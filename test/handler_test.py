from types import SimpleNamespace

from app.tools import tool_executor
from app.tool_handler import ToolCallHandler


handler = ToolCallHandler(tool_executor)

# Simulate a tool call returned by Groq
mock_tool_call = SimpleNamespace(
    id="call_123",
    function=SimpleNamespace(
        name="count_words",
        arguments='{"text": "Agentic AI is interesting"}',
    ),
)

results = handler.handle([mock_tool_call])

for result in results:
    print(result)