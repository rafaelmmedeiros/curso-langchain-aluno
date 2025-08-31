from email import message
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()

system_message = ("system", "You are an assistant that can answer questions in a {style} style")
user_message = ("user", "{input}")

chat_prompt_template = ChatPromptTemplate([system_message, user_message])

messages = chat_prompt_template.format_messages(style="funny", input="Who was Carl Sagan?")

for message in messages:
    print(f"{message.type}: {message.content}")

model = ChatGoogleGenerativeAI(model="gemini-2.5-pro", temperature=0.5)
response = model.invoke(messages)
print(response.content)