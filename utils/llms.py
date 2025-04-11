import os
import ssl
from langchain_groq import ChatGroq
from dotenv import load_dotenv

# Fix SSL certificate issues
ssl._create_default_https_context = ssl._create_unverified_context
os.environ['SSL_CERT_FILE'] = ''

load_dotenv()

class LLMModel:
    def __init__(self, model_name="gemma2-9b-it"):
        if not model_name:
            raise ValueError("Model is not defined.")
        self.model_name = model_name
        try:
            self.groq_model = ChatGroq(
                model=self.model_name,
                api_key=os.getenv("GROQ_API_KEY"),
                request_timeout=60,
                max_retries=3
            )
        except Exception as e:
            raise RuntimeError(f"Failed to initialize Groq client: {str(e)}")
        
    def get_model(self):
        
        return self.groq_model

if __name__ == "__main__":
    llm_instance = LLMModel()  
    llm_model = llm_instance.get_model()
    response = llm_model.invoke("hi")
    print(response)