# Vehicle Service Assistant 🚗

An intelligent, multi-agent AI assistant designed to provide expert vehicle maintenance advice, diagnostic assistance, and service interval recommendations using RAG (Retrieval-Augmented Generation) and Groq LLM services.

---

## 🌟 Key Features

- 🤖 **Multi-Agent Architecture**: Dedicated agents for intent classification, RAG retrieval, symptom diagnostics, and maintenance scheduling.
- 📚 **Domain-Specific RAG**: Vector database powered by ChromaDB & HuggingFace embeddings for accurate manual lookups.
- ⚡ **Groq LLM Integration**: Fast inference with `llama-3.3-70b-versatile`.
- 📊 **Interactive Streamlit UI**: User-friendly dashboard with vehicle parameter filters, diagnostic cards, and source attribution tabs.
- 🛠️ **Automated Diagnostic & Scheduling**: Tailored recommendations based on mileage, warning indicators, and vehicle specifications.

---

## 🏗️ Architecture Overview

```
               [ User Input / Streamlit UI ]
                             │
                             ▼
                    [ Agent Orchestrator ]
                             │
       ┌─────────────────────┼─────────────────────┐
       ▼                     ▼                     ▼
[ Intent Agent ]    [ Diagnostic Agent ]    [ Schedule Agent ]
       │                     │                     │
       └─────────────────────┼─────────────────────┘
                             ▼
                   [ Knowledge Agent / RAG ]
                             │
                    ( Chroma VectorDB )
                             │
                             ▼
                    [ Groq LLM Engine ]
                             │
                             ▼
                      [ Final Response ]
```

---

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.10+
- Groq API Key (`GROQ_API_KEY`)

### 2. Environment Setup
```bash
# Clone repository
git clone https://github.com/dushananuradha1126-tech/Vehicle-service-assistant.git
cd Vehicle-service-assistant

# Create & activate virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Variables
Create a `.env` file in the root directory:
```env
GROQ_API_KEY=your_groq_api_key_here
```

### 4. Build Vector Store
```bash
python -m rag.ingest
```

### 5. Launch Application
```bash
streamlit run app.py
```

---

## 📁 Project Structure

```
├── agents/               # Multi-agent system (Intent, Knowledge, Diagnostic, Schedule, Orchestrator)
├── documents/            # Vehicle service domain knowledge docs
├── rag/                  # RAG pipeline (Ingest, Retriever)
├── utils/                # Configuration and LLM API clients
├── tests/                # Automated unit test suite
├── app.py                # Streamlit web application interface
└── README.md             # Project documentation
```

---

## 🛡️ License

Distributed under the MIT License.