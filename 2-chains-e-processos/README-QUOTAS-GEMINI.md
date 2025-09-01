# 🚀 ESTRATÉGIAS PARA CONTRORNAR QUOTAS GRATUITAS DO GEMINI

## 📊 Limitações Atuais
- **15 requisições por minuto** (1 a cada 4 segundos)
- **900 requisições por hora**
- **21.600 requisições por dia**

## 🎯 Estratégias Implementadas

### 1. **Rate Limiting Inteligente** (`7-pipeline-de-sumarizacao.py`)
- ✅ Delays automáticos de 4.5s entre chamadas
- ✅ Tratamento de erros de quota
- ✅ Retry automático com backoff
- ✅ Jitter para evitar sincronização

### 2. **Sistema de Fallback** (`8-estrategias-quota-gratuita.py`)
- ✅ Fallback para processamento local quando quota excedida
- ✅ Cache local para evitar reprocessamento
- ✅ Processamento em lotes com delays
- ✅ Múltiplas estratégias combinadas

### 3. **Configuração Otimizada** (`config-quota-otimizada.py`)
- ✅ Monitoramento de quotas em tempo real
- ✅ Cálculo de tempos estimados
- ✅ Dicas de otimização
- ✅ Estratégias avançadas

## 🚀 Como Usar

### Opção 1: Rate Limiting Automático
```python
# Use o arquivo 7-pipeline-de-sumarizacao.py modificado
# Ele já tem rate limiting automático implementado
python 7-pipeline-de-sumarizacao.py
```

### Opção 2: Estratégias Avançadas
```python
# Use o arquivo 8-estrategias-quota-gratuita.py
# Implementa fallbacks e cache local
python 0-estrategias-quota-gratuita.py
```

### Opção 3: Configuração Personalizada
```python
# Use config-quota-otimizada.py para monitorar quotas
python config-quota-otimizada.py
```

## 💡 Dicas Importantes

### ✅ **O QUE FAZER:**
- Use delays de 4.5s entre requisições
- Processe em lotes pequenos (3-5 por vez)
- Implemente cache local
- Use prompts específicos e concisos
- Monitore o uso das quotas

### ❌ **O QUE EVITAR:**
- Muitas chamadas em sequência rápida
- Prompts muito longos
- Reprocessar textos idênticos
- Ignorar erros de quota

## 🔧 Configurações Recomendadas

### Delays Ótimos:
- **Entre requisições**: 4.5 segundos
- **Entre lotes**: 10 segundos
- **Backoff em erro**: 60 segundos

### Tamanhos de Lote:
- **Lote pequeno**: 3-5 itens
- **Lote médio**: 5-10 itens
- **Lote grande**: 10+ itens (com delays maiores)

## 📈 Monitoramento

### Status das Quotas:
```python
from config_quota_otimizada import QuotaMonitor

monitor = QuotaMonitor()
status = monitor.get_quota_status()

print(f"Requisições esta hora: {status['requests_this_hour']}")
print(f"Restantes hoje: {status['daily_remaining']}")
print(f"Pode fazer requisição: {status['can_make_request']}")
```

### Tempo Estimado:
```python
from config_quota_otimizada import estimate_processing_time

tempo = estimate_processing_time(20)  # 20 itens
print(f"Tempo estimado: {tempo/60:.1f} minutos")
```

## 🆘 Soluções para Emergências

### Quando a Quota for Excedida:

1. **Aguarde 60 segundos** (backoff automático)
2. **Use fallback local** (processamento básico)
3. **Reduza o tamanho dos lotes**
4. **Aumente os delays entre chamadas**

### Fallback Local:
```python
def fallback_summary(text):
    """Sumarização básica quando Gemini não está disponível"""
    sentences = text.split('.')
    if len(sentences) > 2:
        return sentences[0] + '. ' + sentences[-2] + '.'
    return text[:200] + '...'
```

## 🔄 Alternativas Gratuitas

### Se o Gemini Continuar com Problemas:

1. **Hugging Face** (modelos gratuitos)
2. **Ollama** (modelos locais)
3. **OpenAI** (créditos gratuitos mensais)
4. **Claude** (versão gratuita limitada)

## 📝 Exemplo de Uso Completo

```python
from langchain_google_genai import ChatGoogleGenerativeAI
import time

class QuotaAwareModel:
    def __init__(self):
        self.model = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")
        self.last_call = 0
        
    def invoke(self, prompt):
        # Aguarda 4.5s entre chamadas
        current_time = time.time()
        if current_time - self.last_call < 4.5:
            time.sleep(4.5 - (current_time - self.last_call))
        
        try:
            result = self.model.invoke(prompt)
            self.last_call = time.time()
            return result
        except Exception as e:
            if "quota" in str(e).lower():
                print("Quota excedida! Aguardando 60s...")
                time.sleep(60)
                return self.invoke(prompt)  # Retry
            raise e

# Uso
model = QuotaAwareModel()
result = model.invoke("Summarize this text...")
```

## 🎉 Resultado Esperado

Com essas estratégias, você deve conseguir:
- ✅ Usar o Gemini gratuitamente sem erros de quota
- ✅ Processar textos de forma eficiente
- ✅ Ter fallbacks quando necessário
- ✅ Monitorar o uso das quotas
- ✅ Economizar tokens e requisições

## 🚨 Lembre-se

- **NUNCA** pague pelo Gemini se você pode usar gratuitamente
- **SEMPRE** implemente rate limiting
- **SEMPRE** tenha fallbacks
- **MONITORE** o uso das quotas
- **SEJA PACIENTE** - os delays são necessários

---

**💡 Dica Final**: Use o Cursor (que você já paga) para desenvolvimento e o Gemini gratuito para IA, com as estratégias de quota implementadas!
