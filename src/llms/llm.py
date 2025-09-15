from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv



class GroqLLM:
    """
    Wrapper class for ChatGroq language model.
    """
    def __init__(self):
        load_dotenv()

    def getllm(self, model_name: str = "llama-3.3-70b-versatile"):
        try:
            os.environ["GROQ_API_KEY"] = self.GROQ_API_KEY=os.getenv("GROQ_API_KEY")
            llm = ChatGroq(api_key=self.GROQ_API_KEY, model=model_name)
            return llm
        except Exception as e:
            print(f"Error initializing ChatGroq: {e}")
            return None   

