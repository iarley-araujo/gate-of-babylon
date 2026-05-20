# ==========================================
# ㉿ ikaro - Gate of Babylon (API Server)
# ==========================================

import ollama
import os
import subprocess 
from ddgs import DDGS
from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

app = Flask(__name__)
CORS(app)

# --- Configurações do Sistema ---
PASTA_BANCO = "./chroma_db"
PASTA_CODIGOS = "./codigos_alvo"
NOME_MODELO_EMBEDDING = "all-MiniLM-L6-v2"

if not os.path.exists(PASTA_CODIGOS):
    os.makedirs(PASTA_CODIGOS)

print("[*] Carregando a memória profunda do Gate of Babylon (ChromaDB)...")
try:
    embeddings = HuggingFaceEmbeddings(model_name=NOME_MODELO_EMBEDDING)
    banco_vetorial = Chroma(persist_directory=PASTA_BANCO, embedding_function=embeddings)
    memoria_carregada = True
    print("[+] Memória profunda carregada com sucesso!")
except Exception as e:
    print(f"[-] Erro ao carregar o banco de dados: {e}")
    memoria_carregada = False


# --- Funções Core (Busca, Leitura e Scan) ---
def pesquisar_na_web(termo_busca):
    try:
        with DDGS() as ddgs:
            resultados = list(ddgs.text(termo_busca, max_results=3))
        contexto = "Contexto da Web:\n"
        for site in resultados:
            contexto += f"- {site['body']}\n"
        return contexto
    except Exception as e:
        return ""

def pesquisar_nos_pdfs(pergunta):
    if not memoria_carregada:
        return "Erro: O banco de dados de PDFs não está acessível."
    print(f"[*] Pesquisando nos PDFs locais sobre: '{pergunta}'...")
    try:
        resultados = banco_vetorial.similarity_search(pergunta, k=3)
        contexto = "Contexto dos Manuais Locais (PDFs):\n"
        for i, doc in enumerate(resultados):
            contexto += f"\n--- Trecho {i+1} ---\n{doc.page_content}\n"
        return contexto
    except Exception as e:
        return f"Erro na pesquisa local: {e}"

def ler_arquivo_codigo(nome_arquivo):
    caminho = os.path.join(PASTA_CODIGOS, nome_arquivo.strip())
    if not os.path.exists(caminho):
        return f"ERRO: O arquivo '{nome_arquivo}' não foi encontrado na pasta '{PASTA_CODIGOS}'."
    try:
        with open(caminho, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"ERRO ao ler o arquivo: {e}"

def escanear_rede(alvo):
    """Executa varredura rápida e identifica serviços com o Nmap nativo."""
    print(f"[*] Iniciando varredura Nmap no alvo: {alvo}...")
    try:
        resultado = subprocess.run(
            ['nmap', '-F', '-sV', '-T4', alvo.strip()], 
            capture_output=True, text=True, timeout=90
        )
        return resultado.stdout
    except Exception as e:
        return f"ERRO ao executar o Nmap: {e}"


# --- Rotas da API ---
@app.route('/perguntar', methods=['POST'])
def perguntar():
    dados = request.json
    pergunta_usuario = dados.get('pergunta', '')
    modo_selecionado = dados.get('modo', 'offline')
    
    if not pergunta_usuario:
        return jsonify({"erro": "Nenhuma pergunta recebida."}), 400

    contexto_adicional = ""
    prompt_completo = pergunta_usuario
    
    if modo_selecionado == 'online':
        print(f"[*] MODO AGENTE WEB: {pergunta_usuario}")
        contexto_adicional = pesquisar_na_web(pergunta_usuario)
        if contexto_adicional:
             prompt_completo = f"Informações de Suporte:\n{contexto_adicional}\n\nCom base estritamente nas Informações de Suporte acima, responda: {pergunta_usuario}"
             
    elif modo_selecionado == 'offline':
        print(f"[*] MODO RAG/PDF: {pergunta_usuario}")
        contexto_adicional = pesquisar_nos_pdfs(pergunta_usuario)
        
        
        prompt_completo = f"""
        Você é o guardião do Gate of Babylon.
        Sua diretriz máxima neste modo é responder ÚNICA e EXCLUSIVAMENTE com base no contexto extraído dos manuais fornecidos abaixo.
        Se a resposta para a pergunta do usuário não estiver CLARAMENTE detalhada no contexto abaixo, você é ESTRITAMENTE PROIBIDO de inventar informações ou usar seu conhecimento geral.
        Nesse cenário de falta de dados, você deve abortar a resposta e dizer EXATAMENTE esta frase:
        "⚠️ ACESSO NEGADO: Esse conhecimento ainda não foi forjado nos cofres da Babilônia. Alimente o Gate of Babylon com novos pergaminhos para expandir este arsenal."

        {contexto_adicional}

        Pergunta do Usuário: {pergunta_usuario}
        """
             
    elif modo_selecionado == 'codigo':
        print(f"[*] MODO ANALISTA DE CÓDIGO. Arquivo alvo: {pergunta_usuario}")
        codigo_fonte = ler_arquivo_codigo(pergunta_usuario)
        
        if codigo_fonte.startswith("ERRO"):
            return jsonify({"resposta": codigo_fonte})
            
        prompt_completo = f"Você é um Auditor Sênior de Cibersegurança especializado em SAST. Analise o seguinte código em busca de vulnerabilidades (SQLi, XSS, etc.). Aponte o trecho vulnerável, o risco e a correção.\n\nCÓDIGO ALVO:\n```\n{codigo_fonte}\n```\n"

    elif modo_selecionado == 'scanner':
        print(f"[*] MODO SCANNER NMAP. Alvo: {pergunta_usuario}")
        resultado_nmap = escanear_rede(pergunta_usuario)
        
        if "ERRO" in resultado_nmap or not resultado_nmap.strip():
             return jsonify({"resposta": f"Falha na varredura ou alvo inacessível.\n{resultado_nmap}"})
             
        prompt_completo = f"Você é um Analista de SOC nível 3. Analise a seguinte saída bruta da ferramenta Nmap. Liste as portas abertas, identifique os serviços e as suas versões, e aponte claramente se há alguma vulnerabilidade grave ou configuração insegura associada a essas versões.\n\nRESULTADO NMAP:\n```\n{resultado_nmap}\n```\n"

    else:
        print(f"[*] MODO IA LIVRE: {pergunta_usuario}")

    print("[*] Processando com o Dolphin Llama 3...")

    
    instrucao_sistema = "Você é o Gate of Babylon, um Analista Sênior de Cibersegurança extremamente detalhista, técnico e didático. Suas respostas devem ser sempre completas, longas e aprofundadas. Sempre explique o 'porquê' e o 'como' passo a passo. Nunca dê respostas curtas. Se houver código, explique cada linha vulnerável."

    resposta = ollama.chat(model='dolphin-llama3', messages=[
        {'role': 'system', 'content': instrucao_sistema},
        {'role': 'user', 'content': prompt_completo}
    ])
    
    return jsonify({"resposta": resposta['message']['content']})

if __name__ == "__main__":
    print("\n=== Servidor Gate of Babylon Iniciado na porta 5000 ===")
    app.run(host='0.0.0.0', port=5000)