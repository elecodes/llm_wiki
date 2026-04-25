import os
from pathlib import Path
from google import genai
from dotenv import load_dotenv

# Path to .env
env_path = Path("llm wiki/scripts/.env")
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("GEMINI_API_KEY")
print(f"Using API Key starting with: {api_key[:8]}...")

client = genai.Client(api_key=api_key)

print("Listing available models...")
try:
    for m in client.models.list():
        print(f"Model: {m.name} (Methods: {m.supported_actions})")
except Exception as e:
    print(f"Error: {e}")
