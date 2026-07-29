import logging
import time
from groq import Groq
from utils.config import GROQ_API_KEY, GROQ_MODEL

logger = logging.getLogger(__name__)

_client = None

def get_groq_client() -> Groq:
    """Returns singleton Groq API client instance."""
    global _client
    if _client is None:
        if not GROQ_API_KEY:
            logger.warning("GROQ_API_KEY is missing or empty.")
            raise ValueError("GROQ_API_KEY environment variable is not set.")
        _client = Groq(api_key=GROQ_API_KEY)
    return _client

def ask_groq(
    prompt: str,
    system_prompt: str = None,
    temperature: float = 0.3,
    max_tokens: int = 1024,
    max_retries: int = 2
) -> str:
    """
    Sends prompt request to Groq LLM service with retry mechanism.
    """
    if system_prompt is None:
        system_prompt = (
            "You are a certified Vehicle Service & Maintenance AI Assistant.\n"
            "Answer questions related to vehicle maintenance, diagnostic troubleshooting, "
            "engine oil, braking systems, battery health, and service intervals."
        )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ]

    for attempt in range(max_retries + 1):
        try:
            client = get_groq_client()
            completion = client.chat.completions.create(
                model=GROQ_MODEL,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return completion.choices[0].message.content
        except Exception as exc:
            logger.warning(f"Groq API call failed (attempt {attempt + 1}/{max_retries + 1}): {exc}")
            if attempt < max_retries:
                time.sleep(1.5)
            else:
                raise RuntimeError(f"Failed to communicate with Groq service after retries: {exc}")

if __name__ == "__main__":
    try:
        ans = ask_groq("What are the primary symptoms of a failing battery?")
        print(ans)
    except Exception as e:
        print(f"Error: {e}")