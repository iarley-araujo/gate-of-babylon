# ㉿ Gate of Babylon

**Gate of Babylon** é uma suíte de automação de segurança que roda 100% local. Ela integra um LLM local (`dolphin-llama3` via Ollama) a um backend em Python para apoiar tarefas de segurança ofensiva e defensiva, sem enviar dados para serviços externos.

![Interface do Gate of Babylon](https://raw.githubusercontent.com/iarley-araujo/iarley-araujo/main/gate-of-babylon.png)

## Funcionalidades

| Modo | O que faz |
|---|---|
| **IA Livre** | Chat com o modelo local para dúvidas de segurança |
| **Ler PDFs (RAG)** | Indexa sua própria documentação técnica em PDF (ChromaDB) e responde com base nela |
| **Agente Web (OSINT)** | Pesquisa em fontes abertas via DuckDuckGo e resume os resultados |
| **Auditar Código (SAST)** | Analisa arquivos em `codigos_alvo/` em busca de SQLi, XSS e padrões inseguros |
| **Scanner Nmap** | Executa `nmap -F -sV` em um alvo e pede ao modelo uma análise das portas e serviços |

## Tecnologias

Python · Flask · Ollama · LangChain · ChromaDB · HuggingFace Embeddings · Nmap · HTML/JS

## Como rodar

**Pré-requisitos:** [Ollama](https://ollama.com/) com o modelo `dolphin-llama3`, Python 3.11+ e Nmap instalado.

```bash
git clone https://github.com/iarley-araujo/gate-of-babylon.git
cd gate-of-babylon

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

ollama pull dolphin-llama3
```

**Adicionar documentação ao RAG** (use PDFs que você tem direito de usar, como suas anotações ou documentação oficial):

```bash
python3 ia_indexer.py caminho/para/documento.pdf
```

**Iniciar o servidor:**

```bash
python3 ia_api.py
```

Depois abra `GateOfBabylon/index.html` no navegador e ajuste a constante `API_URL` para o IP da máquina onde a API está rodando.

## Estrutura

```
ia_api.py         # servidor Flask com os modos de operação
ia_backend.py     # versão de linha de comando
ia_indexer.py     # indexa PDFs no banco vetorial
GateOfBabylon/    # interface web
codigos_alvo/     # arquivos de exemplo para a auditoria (SAST)
chroma_db/        # banco vetorial local (criado automaticamente)
```

## Próximos passos

- [ ] Validar o alvo do scanner (aceitar só IP/hostname) para evitar injeção de argumentos no Nmap
- [ ] Restringir a API a `127.0.0.1` por padrão e limitar o CORS
- [ ] Exportar relatórios das análises em Markdown

## ⚠️ Aviso legal

Projeto para fins educacionais e de segurança ética. Varrer, auditar ou atacar sistemas sem autorização é crime. Use apenas em ambientes próprios ou com permissão por escrito.

---

Desenvolvido por **Iarley Carvalho Araujo** · [LinkedIn](https://www.linkedin.com/in/iarley-carvalho) · [Portfólio](https://springgreen-lion-117087.hostingersite.com)
