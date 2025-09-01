"""
CONFIGURAÇÃO OTIMIZADA PARA QUOTAS GRATUITAS DO GEMINI
=======================================================

Este arquivo contém configurações e dicas para maximizar o uso gratuito
do Gemini sem exceder as quotas.
"""

import os
from typing import Dict, Any

# ============================================================================
# CONFIGURAÇÕES DE QUOTA
# ============================================================================

QUOTA_CONFIG = {
    "requests_per_minute": 15,
    "requests_per_hour": 900,  # 15 * 60
    "requests_per_day": 21600,  # 15 * 60 * 24
    
    # Delays recomendados
    "min_delay_between_requests": 4.5,  # segundos
    "delay_between_batches": 10.0,      # segundos
    "backoff_on_quota_error": 60,       # segundos
    
    # Tamanhos de lote otimizados
    "optimal_batch_size": 3,
    "max_concurrent_requests": 1,
}

# ============================================================================
# DICAS PARA ECONOMIZAR QUOTAS
# ============================================================================

QUOTA_TIPS = [
    "💡 Use cache local para evitar reprocessar textos idênticos",
    "💡 Processe textos em lotes pequenos (3-5 por vez)",
    "💡 Implemente delays de 4.5s entre requisições",
    "💡 Use fallbacks simples quando possível",
    "💡 Evite fazer muitas chamadas em sequência rápida",
    "💡 Monitore o uso das quotas ao longo do dia",
    "💡 Use prompts mais específicos para reduzir tokens",
    "💡 Considere usar modelos menores quando apropriado",
]

# ============================================================================
# ESTRATÉGIAS DE OTIMIZAÇÃO
# ============================================================================

OPTIMIZATION_STRATEGIES = {
    "prompt_optimization": [
        "Seja específico nos prompts para reduzir tokens",
        "Use templates reutilizáveis",
        "Evite prompts muito longos",
        "Use instruções claras e diretas"
    ],
    
    "batch_processing": [
        "Processe múltiplos itens em uma única chamada quando possível",
        "Use delays entre lotes para distribuir a carga",
        "Implemente retry logic com backoff exponencial"
    ],
    
    "caching": [
        "Cache local para resultados frequentes",
        "Cache de embeddings para textos similares",
        "Evite reprocessar conteúdo idêntico"
    ],
    
    "fallback_strategies": [
        "Implemente lógica de fallback para quando a quota for excedida",
        "Use algoritmos simples como backup",
        "Processe em modo offline quando possível"
    ]
}

# ============================================================================
# MONITORAMENTO DE QUOTA
# ============================================================================

class QuotaMonitor:
    def __init__(self):
        self.request_count = 0
        self.last_reset = time.time()
        self.hourly_requests = 0
        self.daily_requests = 0
        
    def can_make_request(self) -> bool:
        """Verifica se ainda pode fazer requisições"""
        current_time = time.time()
        
        # Reset contadores a cada hora/dia
        if current_time - self.last_reset >= 3600:  # 1 hora
            self.hourly_requests = 0
            self.last_reset = current_time
            
        if current_time - self.last_reset >= 86400:  # 1 dia
            self.daily_requests = 0
            
        return (self.hourly_requests < QUOTA_CONFIG["requests_per_hour"] and
                self.daily_requests < QUOTA_CONFIG["requests_per_day"])
    
    def record_request(self):
        """Registra uma requisição feita"""
        self.request_count += 1
        self.hourly_requests += 1
        self.daily_requests += 1
        
    def get_quota_status(self) -> Dict[str, Any]:
        """Retorna status atual das quotas"""
        return {
            "requests_this_hour": self.hourly_requests,
            "requests_today": self.daily_requests,
            "hourly_remaining": QUOTA_CONFIG["requests_per_hour"] - self.hourly_requests,
            "daily_remaining": QUOTA_CONFIG["requests_per_day"] - self.daily_requests,
            "can_make_request": self.can_make_request()
        }

# ============================================================================
# FUNÇÕES UTILITÁRIAS
# ============================================================================

def calculate_optimal_delay(total_requests: int, time_window_minutes: int = 60) -> float:
    """
    Calcula o delay ótimo entre requisições para distribuir uniformemente
    """
    if total_requests <= 0:
        return 0
    
    # Distribui as requisições uniformemente no tempo disponível
    time_window_seconds = time_window_minutes * 60
    optimal_delay = time_window_seconds / total_requests
    
    # Adiciona margem de segurança
    return max(optimal_delay + 1, QUOTA_CONFIG["min_delay_between_requests"])

def estimate_processing_time(num_items: int, batch_size: int = None) -> float:
    """
    Estima o tempo total de processamento considerando delays
    """
    if batch_size is None:
        batch_size = QUOTA_CONFIG["optimal_batch_size"]
    
    num_batches = (num_items + batch_size - 1) // batch_size
    
    # Tempo por item (incluindo delay)
    time_per_item = QUOTA_CONFIG["min_delay_between_requests"]
    
    # Tempo entre lotes
    time_between_batches = QUOTA_CONFIG["delay_between_batches"]
    
    # Tempo total estimado
    total_time = (num_items * time_per_item) + ((num_batches - 1) * time_between_batches)
    
    return total_time

# ============================================================================
# EXEMPLO DE USO
# ============================================================================

def exemplo_configuracao():
    """Exemplo de como usar as configurações de quota"""
    
    print("🔧 CONFIGURAÇÃO DE QUOTA OTIMIZADA")
    print("=" * 50)
    
    # Mostra configurações
    print(f"📊 Requisições por minuto: {QUOTA_CONFIG['requests_per_minute']}")
    print(f"📊 Requisições por hora: {QUOTA_CONFIG['requests_per_hour']}")
    print(f"📊 Requisições por dia: {QUOTA_CONFIG['requests_per_day']}")
    
    print("\n💡 DICAS PARA ECONOMIZAR QUOTAS:")
    for tip in QUOTA_TIPS:
        print(f"   {tip}")
    
    print("\n⚡ ESTRATÉGIAS DE OTIMIZAÇÃO:")
    for category, strategies in OPTIMIZATION_STRATEGIES.items():
        print(f"\n   {category.upper()}:")
        for strategy in strategies:
            print(f"     • {strategy}")
    
    # Exemplo de cálculo de tempo
    num_items = 20
    estimated_time = estimate_processing_time(num_items)
    print(f"\n⏱️  TEMPO ESTIMADO:")
    print(f"   Para processar {num_items} itens: {estimated_time/60:.1f} minutos")
    
    # Exemplo de monitoramento
    monitor = QuotaMonitor()
    status = monitor.get_quota_status()
    print(f"\n📈 STATUS ATUAL:")
    print(f"   Requisições restantes esta hora: {status['hourly_remaining']}")
    print(f"   Requisições restantes hoje: {status['daily_remaining']}")
    print(f"   Pode fazer requisição: {'✅ Sim' if status['can_make_request'] else '❌ Não'}")

if __name__ == "__main__":
    import time
    exemplo_configuracao()
