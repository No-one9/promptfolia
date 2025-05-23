import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

print("Available models for your API key:")
for m in genai.list_models():
    # Let's check if the model supports the 'generateContent' method.
    # The name in m.name is what you need to use.
    if 'generateContent' in m.supported_generation_methods:
        print(f"Model name: {m.name}")
        print(f"  Supported generation methods: {m.supported_generation_methods}")
        print(f"  Display name: {m.display_name}")
        print("-" * 30)