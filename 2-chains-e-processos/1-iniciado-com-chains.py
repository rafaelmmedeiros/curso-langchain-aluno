from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-2.5-pro", temperature=0.5)

question_template = PromptTemplate(
    input_variables=["name"],
    template="Hi, I'm {name}! Tell a joke about my name!"
)

question_chain = question_template | model

response = question_chain.invoke({"name": "John"})
print(response.content)
