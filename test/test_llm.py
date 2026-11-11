from app.core.config import settings
from app.llm import GroqLLM

from app.tools import (
    tool_registry,
    tool_schema_generator,
)

llm = GroqLLM()

available_tools = [
    tool_schema_generator.generate(function)
    for function in tool_registry.get_all_tools()
]

messages = [
    {
        "role": "user",
        "content": "How many words are in this sentence: "
                   "'Agentic AI systems can use external tools'?"
    }
]

response = llm.generate(
    messages=messages,
    tools=available_tools,
)

message = response.choices[0].message
print("Content:", message.content)
print("Tool calls:", message.tool_calls)
print("Finish reason:", response.choices[0].finish_reason)