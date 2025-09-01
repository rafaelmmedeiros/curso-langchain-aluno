from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
from dotenv import load_dotenv
load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", temperature=0)

long_text = """
The universe began approximately 13.8 billion years ago with the Big Bang, an unimaginably hot and dense state that rapidly expanded. In the first few moments, fundamental forces separated, and subatomic particles formed. Within minutes, hydrogen and helium nuclei were created through nuclear fusion. For hundreds of thousands of years, the universe remained too hot for atoms to form, existing as a plasma of charged particles.
Around 380,000 years after the Big Bang, the universe cooled enough for electrons to combine with nuclei, forming the first neutral atoms. This allowed light to travel freely, creating the cosmic microwave background radiation we can still detect today. Over the next billion years, gravity caused matter to clump together, forming the first stars and galaxies.
Our Milky Way galaxy formed about 13.6 billion years ago, and our solar system began taking shape around 4.6 billion years ago from a cloud of gas and dust. Earth formed through the accretion of smaller bodies, and was initially molten due to intense heat from impacts and radioactive decay. The Moon formed when a Mars-sized object collided with early Earth, ejecting material that eventually coalesced into our satellite.
Life on Earth began around 3.5-4 billion years ago, possibly in hydrothermal vents or shallow pools. The first life forms were simple single-celled organisms that could survive in Earth's harsh early environment. Over billions of years, through natural selection and genetic mutations, life diversified into the incredible variety we see today.
The first multicellular organisms appeared around 600 million years ago, leading to the Cambrian explosion of life forms. Dinosaurs dominated the land for 165 million years until a massive asteroid impact 66 million years ago caused their extinction. This allowed mammals to diversify and eventually led to the evolution of humans.
Modern humans (Homo sapiens) evolved in Africa around 300,000 years ago. We developed language, tools, and culture, eventually spreading across the globe. The agricultural revolution around 10,000 years ago allowed humans to settle in permanent communities, leading to the development of civilizations, writing, and complex societies.
The industrial revolution in the 18th and 19th centuries transformed human society through technological innovation, leading to unprecedented population growth and environmental changes. Today, we face challenges of climate change, resource depletion, and the need to balance human development with environmental sustainability.
Throughout this vast cosmic and biological history, Earth has been the only known planet to harbor life, making it a precious and unique world in our vast universe. Our understanding of this history continues to evolve as new discoveries are made in astronomy, geology, biology, and archaeology.
"""

splitter = RecursiveCharacterTextSplitter(chunk_size=250, chunk_overlap=50)
chunks = splitter.create_documents([long_text])

map_prompt = PromptTemplate.from_template("Write a concise summary of the following text:\n {context}")
map_chain = map_prompt | model | StrOutputParser()

prepare_map_inputs = RunnableLambda(lambda docs: [{"context": doc.page_content} for doc in docs])
map_stage = prepare_map_inputs | map_chain.map()

reduce_prompt = PromptTemplate.from_template("Combine the following summaries into a single concise summary:\n {context}")
reduce_chain = reduce_prompt | model | StrOutputParser()

prepare_reduce_inputs = RunnableLambda(lambda summaries: {"context": "\n".join(summaries)})
pipeline = map_stage | prepare_reduce_inputs | reduce_chain

result = pipeline.invoke(chunks)
print(result)