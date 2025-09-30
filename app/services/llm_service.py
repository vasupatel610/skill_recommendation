# from groq import Groq
# from app.config import Config

# class LLMService:
#     def __init__(self):
#         self.client = Groq(api_key=Config.GROQ_API_KEY)

#     def generate(self, prompt: str) -> str:
#         """Generate text using Groq's LLM."""
#         response = self.client.chat.completions.create(
#             model="llama-3.3-70b-versatile",  # Free model from Groq
#             messages=[
#                 {"role": "system", "content": "You are a skill recommendation assistant."},
#                 {"role": "user", "content": prompt}
#             ],
#             max_tokens=500
#         )
#         return response.choices[0].message.content


from groq import Groq
from app.config import Config

class LLMService:
    def __init__(self):
        self.client = Groq(api_key=Config.GROQ_API_KEY)

    def generate(self, prompt: str) -> str:
        """Generate text using Groq's LLM."""
        response = self.client.chat.completions.create(
            model=Config.GROQ_MODEL,  # Use grok-llama-3.3-70b-versatile
            messages=[
                {"role": "system", "content": "You are a skill recommendation assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )
        return response.choices[0].message.content # type: ignore