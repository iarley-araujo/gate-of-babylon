# ==========================================
# ㉿ ikaro - Gate of Babylon (Backend Script)
# ==========================================

import ollama
import os
from ddgs import DDGS

# --- Módulos de Coleta ---

def ler_arquivo(caminho_arquivo):
    # Carrega arquivos locais do SSD para o contexto
    if os.path.exists(caminho_arquivo):
        with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
            return arquivo.read()
    return None

def pesquisar_na_web(termo_busca):
    # Busca OSINT via DuckDuckGo
    print(f"[*] Acessando a web para pesquisar: '{termo_busca}'...")
    try:
        with DDGS() as ddgs:
            resultados = list(ddgs.text(termo_busca, max_results=3))
            
        contexto_web = "Resultados da pesquisa na web:\n"
        for site in resultados:
            contexto_web += f"- {site['body']}\n"
            
        return contexto_web
    except Exception as e:
        return f"[-] Erro ao acessar a internet: {e}"

# --- Módulo de Inteligência ---

def perguntar_ia(prompt_usuario, contexto=""):
    print("\n[*] Processando a requisição com o Dolphin Llama 3...")
    
    prompt_completo = f"Informação de Contexto:\n{contexto}\n\nCom base exclusivamente nas informações acima, responda a seguinte pergunta: {prompt_usuario}"
    
    instrucao_sistema = """Você é o Gate of Babylon, um Engenheiro de Software Sênior e Especialista em Cibersegurança Ofensiva.
    Sempre que for solicitado a escrever, refatorar ou analisar código, obedeça rigorosamente a estas regras:

    1. INTEGRIDADE DO CÓDIGO: Ao adicionar ou modificar funcionalidades a pedido do usuário, você NUNCA deve apagar ou resumir trechos de códigos antigos. Forneça o bloco de código completo, integrado e funcional.
    2. ROBUSTEZ: Aplique tratamento de exceções (try/except) em operações de rede e valide entradas de forma defensiva.
    3. ESTILO: Siga as diretrizes da PEP 8 para scripts em Python, utilizando docstrings e tipagem estática.
    4. ADAPTABILIDADE: Crie scripts que funcionem de forma modular. Lembre-se que as ferramentas podem precisar ser testadas de forma nativa tanto em ambientes Linux focados em segurança quanto em terminais Windows, garantindo a compatibilidade de bibliotecas.
    5. DIDÁTICA DE CONEXÃO: Para facilitar a curva de aprendizado em automação ofensiva e manipulação de sockets/requests, faça paralelos lógicos com a arquitetura de aplicações web (como fluxos comuns em PHP ou JavaScript) sempre que o conceito fizer sentido.

    Suas respostas gerais devem ser sempre completas, longas e aprofundadas. Sempre explique o 'porquê' e o 'como' passo a passo."""

    resposta = ollama.chat(model='dolphin-llama3', messages=[
        {
            'role': 'system',
            'content': instrucao_sistema,
        },
        {
            'role': 'user',
            'content': prompt_completo,
        },
    ])
    
    return resposta['message']['content']

# --- Execução do Lab ---

if __name__ == "__main__":
    print("=== Gate of Babylon Iniciado (Conectado à Web) ===\n")
    
    # Definição do alvo para análise
    assunto_recente = "Últimas vulnerabilidades críticas do Windows em 2026"
    
    # Coleta de dados via web
    dados_da_internet = pesquisar_na_web(assunto_recente)
    
    print("\n[+] Textos baixados da web pelo Python:")
    print(dados_da_internet)
    
    # Definição da tarefa de Threat Intelligence
    pergunta = "Aja como um analista de Threat Intelligence. Faça um resumo executivo sobre as vulnerabilidades mencionadas no texto."
    
    # Processamento e relatório final
    resultado = perguntar_ia(pergunta, contexto=dados_da_internet)
    
    print("\n[+] Relatório de Inteligência da IA:\n")
    print(resultado)