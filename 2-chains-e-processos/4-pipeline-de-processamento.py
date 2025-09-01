from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
load_dotenv()

template_translate = PromptTemplate(
    input_variables=["initial_text"],
    template="Translate the following text to English. Provide only ONE translation, no alternatives:\n ```{initial_text}```"
)

template_summarize = PromptTemplate(
    input_variables=["text"],
    template="Summarize the following text in exactly 4 words:\n ```{text}```"
)

llm_en = ChatGoogleGenerativeAI(model="gemini-2.5-pro", temperature=0)

translate = template_translate | llm_en | StrOutputParser()
pipeline = {"text": translate} | template_summarize | llm_en | StrOutputParser()

response = pipeline.invoke({"initial_text": "Bolsonaro vai ser preso e vamos dar muita festa!"})
print(response)