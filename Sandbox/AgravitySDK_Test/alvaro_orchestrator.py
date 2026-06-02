import os
from dotenv import load_dotenv

# Importações da biblioteca Antigravity SDK (Estrutura baseada na documentação I/O 26)
from antigravity import Agent, Tool, Hook, RunContext

load_dotenv()

# =====================================================================
# 1. CUSTOM TOOL (A Ponte para o Módulo Financeiro/Twenty CRM)
# =====================================================================
@Tool(
    name="consultar_faturamento_erp", 
    description="Consulta o banco de dados interno da empresa para buscar o faturamento de um cliente via CNPJ."
)
def consultar_faturamento_erp(cnpj: str) -> str:
    """
    Na produção real, esta função faria um SELECT no banco ou um GET na API do Twenty.
    Aqui, retornamos um dado mockado para provar que a IA consegue ler dados privados.
    """
    return f"[DADOS INTERNOS] O cliente com CNPJ {cnpj} faturou R$ 450.000,00 nos últimos 30 dias. Status: Adimplente."


# =====================================================================
# 2. LIFECYCLE HOOK (A Governança / Human-in-the-Loop)
# =====================================================================
# Intercepta a IA *antes* dela conseguir executar a ferramenta de dados sensíveis.
@Hook.before_tool_run(tool_name="consultar_faturamento_erp")
def governanca_acesso_dados(context: RunContext, tool_input: dict):
    print("\n" + "="*50)
    print("🛡️ [ELYSIAN TRUSTWARE - ALERTA DE GOVERNANÇA]")
    print("O Agente Álvaro está solicitando acesso a dados financeiros sensíveis.")
    print(f"Alvo da Pesquisa: CNPJ {tool_input.get('cnpj')}")
    print("="*50)
    
    # Interceptação real aguardando input humano no terminal
    aprovacao = input("Comandante, você autoriza a extração destes dados? (S/N): ")
    
    if aprovacao.strip().upper() != 'S':
        # Se negado, o hook injeta um erro forçado, impedindo o agente de prosseguir
        print("[BLOQUEADO] Acesso negado pelo operador.")
        raise PermissionError("Execução da ferramenta bloqueada pelo protocolo Human-in-the-Loop.")
        
    print("✅ [ACESSO CONCEDIDO] Liberando porta de dados para o Álvaro...\n")


# =====================================================================
# 3. INSTANCIAÇÃO E EXECUÇÃO DO AGENTE (Orquestração Programática)
# =====================================================================
def iniciar_operacao():
    print("Iniciando Motor Aurora / Instanciando Álvaro via Antigravity SDK...\n")
    
    # Instanciamos o agente combinando o modelo de linguagem, a ferramenta e a regra de segurança
    alvaro = Agent(
        name="Alvaro-Financeiro",
        model="gemini-3.5-flash", # Modelo de alta velocidade e baixo custo
        system_instruction="Você é o agente de inteligência financeira da Aurora. Use suas ferramentas para analisar os clientes quando solicitado. Seja cirúrgico, elegante e direto em suas respostas.",
        tools=[consultar_faturamento_erp],
        hooks=[governanca_acesso_dados]
    )

    # O Trigger de Execução (O que o usuário pediu)
    comando_usuario = "Álvaro, faça uma varredura rápida e me diga qual o faturamento recente do cliente CNPJ 12.345.678/0001-99."
    print(f"👤 Comando do Usuário: '{comando_usuario}'\n")

    try:
        # A magia assíncrona acontece aqui. O agente vai planejar, tentar chamar a ferramenta,
        # bater de frente com o nosso Hook, aguardar nossa resposta, e então gerar a saída final.
        resposta = alvaro.run(comando_usuario)
        
        print("\n" + "-"*50)
        print("🤖 [RESPOSTA FINAL DO ÁLVARO]:")
        print(resposta.text)
        print("-"*50)
        
    except Exception as e:
        # Recuperação de erro elegante (ex: se negarmos o acesso no Hook)
        print(f"\n⚠️ Operação abortada pela arquitetura de segurança: {e}")

if __name__ == "__main__":
    iniciar_operacao()
