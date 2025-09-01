from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from dotenv import load_dotenv
load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-2.5-pro", temperature=0)

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

text_splitter = RecursiveCharacterTextSplitter(chunk_size=250, chunk_overlap=70)
chunks = text_splitter.split_text(long_text)
print(len(chunks))
print(chunks[0])
print(chunks[1])
print(chunks[2])
print(chunks[3])
print(chunks[4])
print(chunks[5])
print(chunks[6])
print(chunks[7])