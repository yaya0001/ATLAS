import json
from typing import Any

from app.tools import ToolExecutor


class ToolCallHandler:

    def __init__(self, executor: ToolExecutor): #dependency injection of the ToolExecutor instance into the ToolCallHandler class. This allows the handler to use the executor to execute tool calls.
        self.executor = executor

    def handle(self, tool_calls: list[Any]) -> list[dict]:

        tool_messages = []

        for tool_call in tool_calls:

            call_id = tool_call.id
            function_name = tool_call.function.name
            raw_arguments = tool_call.function.arguments

            try:
                # 1. Parse JSON arguments
                arguments = json.loads(raw_arguments) #Deserialization(from JSON string to Python object) of the raw arguments string into a Python dictionary using json.loads. This allows the handler to work with the arguments in a structured format.

                if not isinstance(arguments, dict):
                    raise ValueError(
                        "Tool arguments must be a JSON object."
                    )

                # 2. Execute the requested tool
                result = self.executor.execute(
                    name=function_name,
                    arguments=arguments,
                )

                # 3. Format the result (from Python object to JSON string)
                content = json.dumps(
                    {"result": result},
                    ensure_ascii=False,#to ensure that the resulting JSON string can contain non-ASCII characters, such as Unicode characters, without escaping them. This is important for preserving the original content of the result, especially if it includes text in languages other than English or special symbols.
                    default=str,#some Python objects (like datetime, Decimal, etc.) are not directly serializable to JSON. By providing default=str, any non-serializable object will be converted to its string representation during serialization. This prevents serialization errors and ensures that the result can be represented as a JSON string.
                )

            except Exception as error:

                content = json.dumps(
                    {
                        "error": str(error),
                        "tool": function_name,
                    },
                    ensure_ascii=False,
                )

            # 4. Create a message for the LLM
            tool_messages.append({
                "role": "tool",
                "tool_call_id": call_id,
                "name": function_name,
                "content": content,
            })

        return tool_messages