from langchain_core.runnables import RunnableLambda

def parse_number(text: str) -> int:
    return int(text.strip())

runnable = RunnableLambda(parse_number)

print(runnable.invoke("123"))