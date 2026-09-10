import os 
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL")

if not GROQ_API_KEY:
    raise EnvironmentError(
        "KEY is not present in the environment. Please add your GROQ API KEY "
    )

def get_llm(temperature: float = 0.2, model: str = GROQ_MODEL) -> ChatGroq:
    return ChatGroq(
        model= model,
        temperature= temperature,
        api_key= GROQ_API_KEY
    )