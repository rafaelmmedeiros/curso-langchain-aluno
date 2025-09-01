"""
ESTRATÉGIAS PARA CONTRORNAR QUOTAS GRATUITAS DO GEMINI
=======================================================

Este arquivo contém várias estratégias para usar o Gemini gratuitamente
sem exceder as quotas de 15 requisições por minuto.
"""

import time
import random
import os
from typing import List, Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# ============================================================================
# ESTRATÉGIA 1: Rate Limiting Inteligente com Backoff Exponencial
# ============================================================================

class SmartRateLimiter:
    def __init__(self, requests_per_minute=15):
        self.requests_per_minute = requests_per_minute
        self.min_interval = 60.0 / requests_per_minute
        self.last_request_time = 0
        self.consecutive_failures = 0
        self.max_retries = 3
        
    def wait_if_needed(self):
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.min_interval:
            wait_time = self.min_interval - time_since_last
            # Adiciona jitter para evitar thundering herd
            wait_time += random.uniform(0, 1)
            print(f"⏳ Aguardando {wait_time:.1f}s...")
            time.sleep(wait_time)
    
    def handle_quota_error(self):
        self.consecutive_failures += 1
        # Backoff exponencial: 60s, 120s, 240s
        wait_time = 60 * (2 ** (self.consecutive_failures - 1))
        print(f"🚫 Quota excedida! Aguardando {wait_time}s...")
        time.sleep(wait_time)
    
    def reset_failures(self):
        self.consecutive_failures = 0

# ============================================================================
# ESTRATÉGIA 2: Modelo com Fallback para Texto Simples
# ============================================================================

class FallbackModel:
    def __init__(self, model_name="gemini-2.5-flash-lite"):
        self.model = ChatGoogleGenerativeAI(model=model_name, temperature=0)
        self.rate_limiter = SmartRateLimiter()
        
    def invoke(self, prompt, max_retries=3):
        for attempt in range(max_retries):
            try:
                self.rate_limiter.wait_if_needed()
                result = self.model.invoke(prompt)
                self.rate_limiter.reset_failures()
                return result
                
            except Exception as e:
                error_msg = str(e).lower()
                if "quota" in error_msg or "429" in error_msg:
                    self.rate_limiter.handle_quota_error()
                    if attempt == max_retries - 1:
                        print("⚠️  Usando fallback de texto simples...")
                        return self._simple_fallback(prompt)
                else:
                    raise e
        
        return self._simple_fallback(prompt)
    
    def _simple_fallback(self, prompt):
        """Fallback simples quando o Gemini não está disponível"""
        # Implementa lógica básica de sumarização
        text = str(prompt)
        words = text.split()
        if len(words) > 100:
            # Pega as primeiras e últimas frases
            sentences = text.split('.')
            if len(sentences) > 2:
                summary = sentences[0] + '. ' + sentences[-2] + '.'
                return type('obj', (object,), {'content': summary})()
        
        return type('obj', (object,), {'content': text[:200] + '...' if len(text) > 200 else text})()

# ============================================================================
# ESTRATÉGIA 3: Processamento em Lotes com Delays
# ============================================================================

def process_in_batches(items: List, batch_size: int = 3, delay_between_batches: float = 10.0):
    """
    Processa itens em lotes com delays entre eles para respeitar quotas
    """
    results = []
    
    for i in range(0, len(items), batch_size):
        batch = items[i:i + batch_size]
        print(f"📦 Processando lote {i//batch_size + 1}/{(len(items) + batch_size - 1)//batch_size}")
        
        # Processa o lote atual
        for item in batch:
            # Aqui você processaria cada item
            results.append(item)
            time.sleep(4.5)  # 4.5s entre itens (15/min = 4s, mas vamos ser conservadores)
        
        # Delay entre lotes
        if i + batch_size < len(items):
            print(f"⏸️  Aguardando {delay_between_batches}s entre lotes...")
            time.sleep(delay_between_batches)
    
    return results

# ============================================================================
# ESTRATÉGIA 4: Cache Local para Evitar Chamadas Repetidas
# ============================================================================

class LocalCache:
    def __init__(self):
        self.cache = {}
    
    def get(self, key):
        return self.cache.get(key)
    
    def set(self, key, value):
        self.cache[key] = value
    
    def has(self, key):
        return key in self.cache

# ============================================================================
# ESTRATÉGIA 5: Uso de Múltiplas Contas (se disponível)
# ============================================================================

class MultiAccountModel:
    def __init__(self, api_keys: List[str]):
        self.models = []
        self.current_index = 0
        
        for api_key in api_keys:
            # Aqui você configuraria cada modelo com uma API key diferente
            # model = ChatGoogleGenerativeAI(..., google_api_key=api_key)
            pass
    
    def get_next_model(self):
        # Rotaciona entre as contas disponíveis
        model = self.models[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.models)
        return model

# ============================================================================
# EXEMPLO DE USO
# ============================================================================

def exemplo_uso_inteligente():
    """Exemplo de como usar as estratégias combinadas"""
    
    # 1. Usa o modelo com fallback
    model = FallbackModel()
    
    # 2. Cache local
    cache = LocalCache()
    
    # 3. Processamento em lotes
    textos = [
        "Primeiro texto para processar...",
        "Segundo texto para processar...",
        "Terceiro texto para processar...",
        "Quarto texto para processar...",
        "Quinto texto para processar..."
    ]
    
    resultados = []
    
    for i, texto in enumerate(textos):
        # Verifica cache primeiro
        cache_key = f"processed_{hash(texto)}"
        if cache.has(cache_key):
            print(f"📋 Usando resultado do cache para texto {i+1}")
            resultados.append(cache.get(cache_key))
            continue
        
        # Processa com o modelo
        print(f"🤖 Processando texto {i+1}/{len(textos)}")
        resultado = model.invoke(texto)
        resultados.append(resultado)
        
        # Salva no cache
        cache.set(cache_key, resultado)
        
        # Delay entre processamentos
        if i < len(textos) - 1:
            print("⏳ Aguardando 5 segundos...")
            time.sleep(5)
    
    return resultados

if __name__ == "__main__":
    print("🚀 Testando estratégias de quota gratuita...")
    resultados = exemplo_uso_inteligente()
    print(f"✅ Processados {len(resultados)} textos com sucesso!")
