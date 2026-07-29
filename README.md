# Vehicle Service Assistant

A multi-agent AI application that helps vehicle owners and mechanics diagnose vehicle issues, check maintenance schedules, estimate repair costs, and look up service manuals using RAG (Retrieval-Augmented Generation) and Groq.

Built with Python, Streamlit, LangChain, ChromaDB, and Groq's Llama 3 model.

---

## What It Does

This project splits user questions into specific categories and passes them to specialized AI agents:

- **Intent Agent**: Figures out what the user is asking (diagnostics, schedule, costs, or general info).
- **Knowledge Agent (RAG)**: Searches local vehicle maintenance manuals stored in ChromaDB to answer technical questions accurately.
- **Diagnostic Agent**: Analyzes reported warning lights, unusual sounds, and engine symptoms to suggest probable causes and safety steps.
- **Schedule Agent**: Generates service checklists based on current mileage and vehicle type.
- **Cost Estimator Agent**: Provides estimated price ranges for parts, labor hours, and repair jobs.

---

## Project Architecture

1. **User Request** (Streamlit UI) -> **Orchestrator** (`agents/orchestrator.py`)
2. **Intent Classification** (`agents/intent_agent.py`) -> Routes to appropriate agent
3. **Context Retrieval** (`rag/retriever.py`) -> Pulls relevant text chunks from `documents/` via ChromaDB
4. **LLM Processing** (`utils/groq_client.py`) -> Generates formatted response using Groq (`llama-3.3-70b-versatile`)

---

## Setup & Installation

### Prerequisites
- Python 3.10 or higher
- Groq API Key (Get one from [Groq Console](https://console.groq.com/))

### 1. Clone the repository
```bash
git clone https://github.com/dushananuradha1126-tech/Vehicle-service-assistant.git
cd Vehicle-service-assistant
```

### 2. Create virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
Create a `.env` file in the root folder:
```env
GROQ_API_KEY=your_actual_groq_api_key_here
```

### 5. Build the vector database
Ingest document manuals into ChromaDB:
```bash
python -m rag.ingest
```

### 6. Run the Streamlit web app
```bash
streamlit run app.py
```

---

## Project Structure

```
Vehicle-service-assistant/
│
├── agents/
│   ├── intent_agent.py        # Classifies user query intent
│   ├── knowledge_agent.py     # RAG document answer synthesizer
│   ├── diagnostic_agent.py    # Symptom & warning light diagnostic agent
│   ├── schedule_agent.py      # Mileage-based maintenance advisor
│   ├── cost_agent.py          # Repair cost & labor estimator agent
│   └── orchestrator.py        # Central agent workflow router
│
├── rag/
│   ├── ingest.py              # Ingests text files into Chroma vector DB
│   └── retriever.py           # Similarity search and prompt context formatter
│
├── documents/                 # Knowledge base manuals (.txt)
├── utils/
│   ├── config.py              # Path and environment variable settings
│   └── groq_client.py         # Groq API client & retry handler
│
├── tests/                     # Unit tests for agents and retriever
├── docs/                      # Technical documentation
├── app.py                     # Main Streamlit UI
└── README.md
```

---

## Running Unit Tests

Run the unit tests to verify agent routing and utility functions:

```bash
python -m unittest discover -s tests
```

---

## License

This project is licensed under the MIT License.