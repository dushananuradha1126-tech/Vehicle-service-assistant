# System Architecture & Multi-Agent Design

## Overview
The Vehicle Service Assistant uses a multi-agent retrieval-augmented generation (RAG) architecture.

```
                    ┌─────────────────────────┐
                    │  Streamlit Dashboard    │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │   Agent Orchestrator    │
                    └────────────┬────────────┘
                                 │
         ┌───────────────────────┼───────────────────────┐
         ▼                       ▼                       ▼
┌──────────────────┐   ┌──────────────────┐   ┌──────────────────┐
│   Intent Agent   │   │ Diagnostic Agent │   │  Schedule Agent  │
└────────┬─────────┘   └────────┬─────────┘   └────────┬─────────┘
         │                      │                      │
         └──────────────────────┼──────────────────────┘
                                ▼
                    ┌─────────────────────────┐
                    │ Knowledge Agent & RAG   │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │   Chroma VectorDB &     │
                    │   Groq LLM Service      │
                    └─────────────────────────┘
```

## Core Components
1. **Agent Orchestrator (`agents/orchestrator.py`)**: Entry point for user queries. Handles workflow coordination.
2. **Intent Agent (`agents/intent_agent.py`)**: Classifies query intent into categories (Diagnostics, Schedule, Specifications, General).
3. **Knowledge Agent (`agents/knowledge_agent.py`)**: Integrates document vector store retrieval with LLM answer synthesis.
4. **Diagnostic Agent (`agents/diagnostic_agent.py`)**: Specializes in mechanical symptoms and severity ratings.
5. **Schedule Agent (`agents/schedule_agent.py`)**: Generates mileage-driven maintenance checklists.
