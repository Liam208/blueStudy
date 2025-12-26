from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

# Load all keys from environment
raw_keys = os.getenv("GEN_AI_KEYS", "")
api_keys = [k.strip() for k in raw_keys.split(",") if k.strip()]
current_key_index = 0


def get_next_client():
    """Cycles to the next available API key and returns a new client."""
    global current_key_index
    if not api_keys:
        raise ValueError("No API keys found in GEN_AI_KEYS environment variable.")

    key = api_keys[current_key_index]
    current_key_index = (current_key_index + 1) % len(api_keys)
    return genai.Client(api_key=key)


# Initialize the first client
client = get_next_client()


def ask_gemini(prompt: str, model: str = "gemini-2.5-flash") -> str:
    global client
    max_retries = len(api_keys)

    for attempt in range(max_retries):
        try:
            response = client.models.generate_content_stream(
                model=model,
                contents=prompt,
            )
            result = ""
            for chunk in response:
                result += chunk.text
            return result

        except Exception as e:
            print(
                f"Error with key {api_keys[(current_key_index-1)%len(api_keys)]}: {e}"
            )

            # Switch to next key for the next attempt
            if attempt < max_retries - 1:
                print("Switching API key and retrying...")
                client = get_next_client()
            else:
                return "All API keys exhausted or failing. Please try again later."
