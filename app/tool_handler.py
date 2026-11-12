import json
from typing import Any
from concurrent.futures import ThreadPoolExecutor

from app.tools import ToolExecutor


class ToolCallHandler:

    def __init__(
        self,
        executor: ToolExecutor,
        max_workers: int = 4,
    ):
        self.executor = executor
        self.max_workers = max_workers

    def _execute_one(self, tool_call: Any) -> dict:

        call_id = tool_call.id
        function_name = tool_call.function.name
        raw_arguments = tool_call.function.arguments

        try:
            arguments = json.loads(raw_arguments)

            if not isinstance(arguments, dict):
                raise ValueError("Tool arguments must be a JSON object.")

            result = self.executor.execute(
                name=function_name,
                arguments=arguments,
            )

            content = json.dumps(
                {"result": result},
                ensure_ascii=False,
                default=str,
            )

        except Exception as error:
            content = json.dumps(
                {
                    "error": str(error),
                    "tool": function_name,
                },
                ensure_ascii=False,
            )

        return {
            "role": "tool",
            "tool_call_id": call_id,
            "name": function_name,
            "content": content,
        }

    def handle(self, tool_calls: list[Any]) -> list[dict]:

        if not tool_calls:
            return []

        with ThreadPoolExecutor(
            max_workers=min(self.max_workers, len(tool_calls))
        ) as executor:

            tool_messages = list(
                executor.map(self._execute_one, tool_calls)
            )

        return tool_messages