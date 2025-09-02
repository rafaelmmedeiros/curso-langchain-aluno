from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate
from utils_gemini import RateLimitedModel
import time

# Usa o modelo com rate limiting (importado do módulo)
model = RateLimitedModel()

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

print(f"📝 Texto dividido em {len(chunks)} chunks para processamento")

# Prompts para sumarização
map_prompt = PromptTemplate.from_template("Write a concise summary of the following text:\n {context}")
reduce_prompt = PromptTemplate.from_template("Combine the following summaries into a single concise summary:\n {context}")

print("🚀 Iniciando pipeline de sumarização...")
print("⚠️  Este processo pode demorar devido aos delays de rate limiting")
print("=" * 50)

# Processa cada chunk individualmente com rate limiting
summaries = []
for i, chunk in enumerate(chunks):
    print(f"📦 Processando chunk {i+1}/{len(chunks)}")
    
    # Cria o prompt para este chunk
    prompt = map_prompt.format(context=chunk.page_content)
    
    # Invoca o modelo com rate limiting (automático!)
    result = model.invoke(prompt)
    
    # Extrai o conteúdo da resposta
    if hasattr(result, 'content'):
        summary = result.content
    else:
        summary = str(result)
    
    summaries.append(summary)
    print(f"✅ Chunk {i+1} processado: {len(summary)} caracteres")
    
    # Delay entre chunks (exceto o último)
    if i < len(chunks) - 1:
        print("⏸️  Aguardando antes do próximo chunk...")
        time.sleep(2)  # Delay adicional entre chunks

print("\n🔄 Combinando sumários...")

# Combina todos os sumários em um único texto
combined_summaries = "\n".join(summaries)

# Cria o prompt para combinação final
final_prompt = reduce_prompt.format(context=combined_summaries)

# Invoca o modelo para combinação final
print("🤖 Gerando sumário final...")
final_result = model.invoke(final_prompt)

# Extrai o resultado final
if hasattr(final_result, 'content'):
    final_summary = final_result.content
else:
    final_summary = str(final_result)

print("\n" + "=" * 50)
print("✅ RESULTADO FINAL:")
print("=" * 50)
print(final_summary)
print("\n" + "=" * 50)
print(f"📊 Estatísticas:")
print(f"   Chunks processados: {len(chunks)}")
print(f"   Sumários gerados: {len(summaries)}")
print(f"   Caracteres no resultado final: {len(final_summary)}")

# Mostra estatísticas do modelo
stats = model.get_stats()
print(f"   Total de requisições ao Gemini: {stats['total_requests']}")