from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.runnables import chain
from dotenv import load_dotenv
load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-2.5-pro", temperature=0.5)

@chain
def square(input_dict: dict) -> dict:
    x = input_dict["x"]
    return {"square_result": x * x}

question_template = PromptTemplate(
    input_variables=["name"],
    template="Hi, I'm {name}! Tell a joke about my name!"
)

question_template2 = PromptTemplate(
    input_variables=["square_result"],
    template="Tell me about the number {square_result}"
)

question_chain = question_template | model
question_chain2 = square | question_template2 | model

response = question_chain2.invoke({"x": 100})
print(response.content)

