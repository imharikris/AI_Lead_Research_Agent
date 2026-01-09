from config import client, GENERATIVE_MODEL
from google.genai import types as genai_types

def call_llm(prompt: str) -> str:
    response = client.models.generate_content(
        model=GENERATIVE_MODEL,
        contents=prompt,
        config=genai_types.GenerateContentConfig(max_output_tokens=300,temperature=0.3 )
    )
    return response.text.strip()