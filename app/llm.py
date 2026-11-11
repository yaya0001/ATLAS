from groq import Groq

from app.core.config import settings


class GroqLLM:

    def __init__(self):
        self.model = settings.model_name
        self.temperature = settings.model_temperature
        self.max_tokens = settings.model_max_tokens

        self.client = Groq(
            api_key=settings.GROQ_API_KEY,
            max_retries=2,
            timeout=30.0,
        )

    def generate(
        self,
        messages: list[dict],
        tools: list[dict] | None = None,
        tool_choice: str = "auto",
    ):

        request_params = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }

        if tools:
            request_params["tools"] = tools
            request_params["tool_choice"] = tool_choice

        response = self.client.chat.completions.create(
            **request_params
        )

        return response