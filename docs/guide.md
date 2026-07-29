# Operational & Deployment Guide

## Setup & Maintenance

### 1. Re-ingesting Manual Documents
When adding new `.txt` files to `documents/`, re-run vector store ingestion:
```bash
python -m rag.ingest
```

### 2. Running Automated Tests
Execute the unit test suite:
```bash
python -m unittest discover -s tests
```

### 3. Launching Streamlit App
```bash
streamlit run app.py
```

### 4. Troubleshooting
- **Missing API Key**: Ensure `GROQ_API_KEY` is present in `.env`.
- **Vector Store Errors**: Delete the `vectorstore/` directory and re-run `python -m rag.ingest`.
