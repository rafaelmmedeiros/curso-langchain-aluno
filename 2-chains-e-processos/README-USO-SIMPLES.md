# 🚀 COMO USAR O RATE LIMITING EM QUALQUER CÓDIGO

## 📋 **O que você precisa fazer:**

### 1. **Copie o arquivo `utils_gemini.py` para a pasta do seu projeto**

### 2. **Importe e use em qualquer código:**

```python
# Importa o modelo com rate limiting
from utils_gemini import RateLimitedModel

# Cria o modelo (rate limiting automático!)
model = RateLimitedModel()

# Usa normalmente - o rate limiting é automático!
result = model.invoke("Seu prompt aqui")
print(result.content)
```

## 🎯 **Exemplos de uso:**

### **Exemplo 1: Pergunta simples**
```python
from utils_gemini import RateLimitedModel

model = RateLimitedModel()
result = model.invoke("O que é Python?")
print(result.content)
```

### **Exemplo 2: Com temperatura personalizada**
```python
from utils_gemini import RateLimitedModel

# Modelo mais criativo
model = RateLimitedModel(temperature=0.7)
result = model.invoke("Escreva uma história criativa sobre um gato")
print(result.content)
```

### **Exemplo 3: Modelo diferente**
```python
from utils_gemini import RateLimitedModel

# Usa outro modelo Gemini
model = RateLimitedModel(model_name="gemini-1.5-pro")
result = model.invoke("Explique a teoria da relatividade")
print(result.content)
```

### **Exemplo 4: Função rápida**
```python
from utils_gemini import create_gemini_model

# Criação rápida
model = create_gemini_model()
result = model.invoke("Diga olá em 5 idiomas")
print(result.content)
```

## 🔧 **Funcionalidades automáticas:**

- ✅ **Rate limiting automático** - 4.5s entre chamadas
- ✅ **Tratamento de erros** - retry automático em caso de quota
- ✅ **Estatísticas** - conta quantas requisições foram feitas
- ✅ **Logs** - mostra o progresso em tempo real

## 📊 **Como ver estatísticas:**

```python
from utils_gemini import RateLimitedModel

model = RateLimitedModel()

# Faz algumas chamadas
result1 = model.invoke("Pergunta 1")
result2 = model.invoke("Pergunta 2")

# Vê estatísticas
stats = model.get_stats()
print(f"Total de requisições: {stats['total_requests']}")
```

## 🚨 **IMPORTANTE:**

- **NUNCA** use `ChatGoogleGenerativeAI` diretamente
- **SEMPRE** use `RateLimitedModel` do módulo
- **NUNCA** se preocupe com quotas - é automático!
- **SEMPRE** importe de `utils_gemini`

## 📁 **Estrutura de arquivos:**

```
seu-projeto/
├── utils_gemini.py          ← Copie este arquivo
├── seu-codigo.py            ← Seu código aqui
├── outro-codigo.py          ← Outro código aqui
└── ...
```

## 🎉 **Resultado:**

- ✅ **Sem erros de quota**
- ✅ **Rate limiting automático**
- ✅ **Código limpo e simples**
- ✅ **Reutilizável em qualquer projeto**

---

**💡 Dica**: Copie o `utils_gemini.py` para cada projeto onde quiser usar o Gemini!
