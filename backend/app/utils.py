import os
import openai

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY

def classify_prompt(message: str) -> str:
    # a structured instruction: ask model to return JSON only
    return (
        "Classify the user message into JSON with keys: category, sentiment, priority, missing_info.\n"
        f"Message: '''{message}''' \n\n"
        "Return only JSON, example: {\"category\":\"account\",\"sentiment\":\"frustrated\",\"priority\":\"high\",\"missing_info\":false}"
    )

def generate_reply_prompt(message: str, classification: dict) -> str:
    return (
        f"You are a helpful support agent. The user message: '''{message}'''.\n"
        f"Classification: {classification}\n"
        "Draft a short professional response (2-4 sentences). Return only the reply text."
    )

# Small wrapper to call OpenAI - you can adapt to other providers or endpoints
def call_openai(prompt: str, max_tokens: int = 150):
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY not set")
    resp = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=0.0
    )
    return resp["choices"][0]["text"].strip()

