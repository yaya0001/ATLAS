from groq import Groq

from core.config import settings


class LLM:
    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY,max_retries=3,timeout=30)
        self.temperature = settings.model_temperature
        self.max_tokens = settings.model_max_tokens
    def generate_text(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=settings.model_name,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )
        return response
