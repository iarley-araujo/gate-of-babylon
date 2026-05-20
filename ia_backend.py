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
    
    resposta = ollama.chat(model='dolphin-llama3', messages=[
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