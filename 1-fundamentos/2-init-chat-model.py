from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

load_dotenv()

gemini_model = init_chat_model("gemini-2.5-pro", model_provider="google_genai")
repsonse_gemini = gemini_model.invoke("Hello, how are you?")

print(repsonse_gemini.content)