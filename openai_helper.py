import os
import openai
from dotenv import load_dotenv
from openai.error import AuthenticationError, RateLimitError, APIConnectionError, OpenAIError


class OpenAIHelper:
    def __init__(self):
        self.load_api_key()

    def load_api_key(self):
        """Load OpenAI API key from .env"""
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise RuntimeError("OPENAI_API_KEY not found in .env file")

        openai.api_key = api_key
        return api_key

    def test_connection(self):
        """Verify API connectivity with a simple prompt"""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Hello, are you working?"}]
            )
            return response.choices[0].message.content

        except AuthenticationError:
            raise RuntimeError("Invalid OpenAI API key")
        except RateLimitError:
            raise RuntimeError("Rate limit exceeded or insufficient credits")
        except APIConnectionError:
            raise RuntimeError("Network connection error")
        except OpenAIError as e:
            raise RuntimeError(f"OpenAI API error: {e}")

    def get_completion(self, prompt: str, model: str = "gpt-3.5-turbo"):
        """Wrapper for OpenAI ChatCompletion API"""
        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content

        except AuthenticationError:
            raise RuntimeError("Invalid OpenAI API key")
        except RateLimitError:
            raise RuntimeError("Rate limit exceeded or insufficient credits")
        except APIConnectionError:
            raise RuntimeError("Network connection error")
        except OpenAIError as e:
            raise RuntimeError(f"OpenAI API error: {e}")