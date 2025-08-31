from langchain.prompts import PromptTemplate

template = PromptTemplate(
    input_variables=["name"],
    template="Hi, I'm {name}! Tell a joke about my name"
)
text = template.format(name="John")
print(text)

