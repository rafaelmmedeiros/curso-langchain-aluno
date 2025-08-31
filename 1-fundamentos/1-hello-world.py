import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

def hello_world_gemini():
    """
    Função principal para demonstrar o uso básico do Gemini via LangChain
    """
    try:
        # Verifica se a API key está configurada
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            print("❌ Erro: GOOGLE_API_KEY não encontrada!")
            print("💡 Dica: Crie um arquivo .env na raiz do projeto e adicione:")
            print("   GOOGLE_API_KEY=sua_chave_api_aqui")
            return
        
        # Inicializa o modelo Gemini
        print("🤖 Inicializando o modelo Gemini...")
        model = ChatGoogleGenerativeAI(
            model="gemini-2.5-pro",
            google_api_key=api_key,
            temperature=0.7
        )
        
        # Lista de mensagens de exemplo
        mensagens_exemplo = [
            "Olá! Como você está?",
            "Conte uma piada engraçada",
            "Explique o que é inteligência artificial em uma frase",
            "Quais são as 3 principais linguagens de programação para iniciantes?"
        ]
        
        print("🚀 Hello World com Gemini!")
        print("=" * 50)
        
        # Testa algumas mensagens
        for i, mensagem in enumerate(mensagens_exemplo, 1):
            print(f"\n📝 Mensagem {i}: {mensagem}")
            print("-" * 30)
            
            # Cria a mensagem
            human_message = HumanMessage(content=mensagem)
            
            # Invoca o modelo
            response = model.invoke([human_message])
            
            # Exibe a resposta
            print(f"🤖 Resposta: {response.content}")
            print()
        
        print("✅ Hello World concluído com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro ao executar o hello world: {str(e)}")
        print("💡 Verifique se sua API key está correta e se você tem acesso ao Gemini")

if __name__ == "__main__":
    hello_world_gemini()