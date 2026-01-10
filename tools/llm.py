from openai import OpenAI
from config import  MODEL_NAME, OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def call_llm(prompt: str) -> str:
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a professional SDR writing high-quality outreach."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
        max_tokens=450,
    )
    return response.choices[0].message.content.strip()