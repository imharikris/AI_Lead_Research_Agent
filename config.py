import os 
from google import genai
from dotenv import load_dotenv
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set.")
client = genai.Client(api_key=GEMINI_API_KEY)
GENERATIVE_MODEL = "gemini-3-flash-preview"
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
 


