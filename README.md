Markdown

# ㉿ Gate of Babylon

**Gate of Babylon** is a high-performance cybersecurity automation suite designed for local execution, ensuring total data privacy and control. The project integrates a local LLM (`dolphin-llama3` via Ollama) with a Python-based backend to process different vectors of offensive and defensive security operations.

## 🛡️ Core Features

* **RAG (Retrieval-Augmented Generation):** Index and query local technical documentation (PDFs) using ChromaDB for intelligent, context-aware answers.
* **SAST (Static Analysis):** Automated code audit module to detect vulnerabilities (SQLi, XSS, insecure patterns) in PHP, JavaScript, and other languages.
* **Web Intelligence (OSINT):** Integrated agent for automated open-source research and threat intelligence gathering via DuckDuckGo.
* **Network Reconnaissance:** Native integration with Nmap to perform rapid port scanning and service version detection.
* **Interface:** A clean, responsive Web UI built with HTML/JS for seamless control of all operation modes.

## 🚀 Getting Started

### Prerequisites
* [Ollama](https://ollama.com/) (running locally)
* Python 3.13+
* Nmap installed on the host system

### Installation
1. Clone this repository:
   ```bash
   git clone [https://github.com/yourusername/gate-of-babylon.git](https://github.com/yourusername/gate-of-babylon.git)
   cd gate-of-babylon

    Create and activate a virtual environment:
    Bash

python3 -m venv venv
source venv/bin/activate

Install dependencies:
Bash

    pip install -r requirements.txt

Configuration

Edit the index.html file to point to your backend server:
JavaScript

// Change this line to your server's IP address
const API_URL = 'http://YOUR_SERVER_IP:5000/perguntar';

🛠️ Usage

    Start the API server on your machine:
    Bash

    python3 ia_api.py

    Open index.html in your browser.

    Select an operation mode (e.g., Scanner, SAST, RAG) and begin your analysis.

📂 Project Structure

    ia_api.py: The core backend server (Flask).

    ia_indexer.py: Script to index new PDF documentation into the vector database.

    index.html: Web-based control panel.

    chroma_db/: Local vector storage (automatically created).

⚠️ Legal Disclaimer

This project is for educational and ethical cybersecurity purposes only. Unauthorized scanning, auditing, or attacking of networks and systems is illegal. Always obtain written permission before performing security testing on any target.

Developed by ㉿ ikaro


### Pro Tip for GitHub:
To ensure your repository remains clean and professional, create a file called `.gitignore` in your project root and add the following line inside it:

```text
chroma_db/
venv/
__pycache__/
.env

This ensures you don't upload unnecessary files or your local database (which can be very large) to GitHub. Your project is now ready to be pushed!
