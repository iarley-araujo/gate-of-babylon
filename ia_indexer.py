# ==========================================
# ㉿ ikaro - Gate of Babylon (Indexer)
# ==========================================

import os
import argparse
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# --- Definições de Storage ---
PASTA_BANCO = "./chroma_db"
NOME_MODELO_EMBEDDING = "all-MiniLM-L6-v2"

def indexar_pdf(caminho_pdf):
    print(f"[*] Iniciando a leitura do arquivo: {caminho_pdf}")
    
    if not os.path.exists(caminho_pdf):
        print("[-] Erro: Arquivo PDF não encontrado!")
        return

    # Extração de dados do documento
    print("[*] Extraindo texto do PDF...")
    loader = PyPDFLoader(caminho_pdf)
    documentos = loader.load()

    # Processamento de chunks para o RAG
    print("[*] Dividindo o texto em blocos...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    blocos = text_splitter.split_documents(documentos)
    print(f"[+] PDF dividido em {len(blocos)} blocos de texto.")

    # Inicialização do motor de embedding
    print("[*] Inicializando o motor de vetorização...")
    embeddings = HuggingFaceEmbeddings(model_name=NOME_MODELO_EMBEDDING)

    # Persistência no ChromaDB
    print("[*] Salvando os dados no ChromaDB no seu SSD...")
    Chroma.from_documents(
        documents=blocos, 
        embedding=embeddings, 
        persist_directory=PASTA_BANCO
    )
    
    print(f"[+] Sucesso! O conhecimento de '{caminho_pdf}' foi adicionado ao Gate of Babylon.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Adicionar conhecimento (PDF) ao Gate of Babylon")
    parser.add_argument("pdf", help="Caminho para o arquivo PDF")
    args = parser.parse_args()
    
    print("=== Gate of Babylon: Indexador de Conhecimento ===")
    indexar_pdf(args.pdf)