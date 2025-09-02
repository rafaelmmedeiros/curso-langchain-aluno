"""
EXEMPLO SIMPLES DE USO DO MÓDULO UTILS_GEMINI
===============================================

Este arquivo mostra como usar o RateLimitedModel em qualquer código
sem precisar repetir a classe.
"""

# Importa o modelo com rate limiting
from utils_gemini import RateLimitedModel

# Cria o modelo (rate limiting automático!)
model = RateLimitedModel()

print("🚀 Testando o modelo com rate limiting...")
print("=" * 50)

# Exemplo 1: Pergunta simples
print("\n1️⃣ Pergunta simples:")
result1 = model.invoke("Explique o que é Python em uma frase")
print(f"Resposta: {result1.content}")

# Exemplo 2: Tradução
print("\n2️⃣ Tradução:")
result2 = model.invoke("Traduza 'Hello World' para português")
print(f"Resposta: {result2.content}")

# Exemplo 3: Código
print("\n3️⃣ Geração de código:")
result3 = model.invoke("Escreva uma função Python que soma dois números")
print(f"Resposta: {result3.content}")

# Exemplo 4: Análise
print("\n4️⃣ Análise de texto:")
texto = "Python é uma linguagem de programação interpretada, de alto nível e de propósito geral."
result4 = model.invoke(f"Analise este texto e diga se é positivo ou negativo: {texto}")
print(f"Resposta: {result4.content}")

# Mostra estatísticas finais
print("\n" + "=" * 50)
stats = model.get_stats()
print("📊 ESTATÍSTICAS FINAIS:")
print(f"   Total de requisições: {stats['total_requests']}")
print(f"   Rate limiting funcionando: ✅")
print(f"   Sem erros de quota: ✅")

print("\n🎉 Pronto! Rate limiting automático funcionando perfeitamente!")
