🤖 AMTICS Chat Bot

A Retrieval-Augmented Generation (RAG) Chatbot built with Ollama, FAISS, and Streamlit, designed to answer questions about the Asha M. Tarsadia Institute of Computer Science and Technology (AMTICS).

🚀 Features

Uses FAISS vector database for semantic search.

Integrates Ollama LLM for answer generation.

Built with a separated backend & frontend architecture.

Provides a simple Streamlit chat UI.

⚙️ Installation
1. Clone Repository

2. Create Virtual Environment
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows

3. Install Dependencies
pip install -r requirements.txt

4. Install & Run Ollama

Install Ollama from https://ollama.com
.

Pull required models:

ollama pull all-minilm
ollama pull llama3:8b

▶️ Running the Chatbot

streamlit run view.py

2. Open in Browser

Streamlit will open automatically at:

http://localhost:8501

📝 Usage

Type your questions in the chatbot.

The system retrieves relevant chunks from info.txt.

LLM generates responses using only retrieved context.

📖 Example Queries

"What programs are offered at AMTICS?"

"Who is the director of AMTICS?"

"Tell me about student clubs."

📌 Requirements

Python 3.8+

Ollama installed & models downloaded

Streamlit

FAISS

PyPDF (if using PDFs as data source)

📜 License

MIT License – feel free to use and modify.
