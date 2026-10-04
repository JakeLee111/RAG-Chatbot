# Heart Health Assistant

A full-stack project that combines a **heart disease prediction model** with a **RAG chatbot**.

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Render-blue)](https://your-app-name.onrender.com)

## Features

- Heart disease probability prediction
- XGBoost machine learning model
- RAG chatbot for heart disease questions
- PostgreSQL + pgvector vector search
- Gemini embeddings and LLM
- React frontend
- FastAPI backend
- Docker support
- Neon PostgreSQL for cloud database

## Architecture

```text
User
 ↓
React
 ↓
FastAPI
 ├── /predict → XGBoost model
 └── /ask → LangChain RAG
                ↓
        PostgreSQL + pgvector
                ↓
              Gemini
```

## Tech Stack

| Area | Technology |
|---|---|
| Frontend | React, Vite |
| Backend | FastAPI, Uvicorn |
| Machine Learning | XGBoost, Joblib |
| RAG | LangChain |
| LLM / Embeddings | Google Gemini |
| Database | PostgreSQL |
| Vector Search | pgvector |
| Cloud Database | Neon |
| Deployment | Docker, Render |

## Project Structure

```text
RAG-Chatbot/
├── app/
│   ├── api.py
│   ├── config.py
│   ├── prediction.py
│   ├── rag.py
│   └── vector_store.py
├── frontend/
├── models/
│   └── heart_model.joblib
├── pdfs/
├── scripts/
│   ├── ingest.py
│   └── setup_db.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Machine Learning Prediction

The XGBoost model is trained separately and exported with Joblib.

```python
joblib.dump(model, "heart_model.joblib")
```

The application loads the trained model and exposes it through:

```http
POST /predict
```

Example response:

```json
{
  "prediction": 0,
  "probability": 0.091
}
```

## RAG Chatbot

PDF documents are split into chunks, converted into embeddings, and stored in PostgreSQL with pgvector.

```text
PDF
 ↓
Text chunks
 ↓
Gemini embeddings
 ↓
PostgreSQL + pgvector
```

For each question:

```text
Question
 ↓
Vector search
 ↓
Relevant document context
 ↓
Gemini
 ↓
Answer
```

API endpoint:

```http
POST /ask
```

## Environment Variables

Create a `.env` file:

```env
GOOGLE_API_KEY=your_api_key
DATABASE_URL=your_neon_database_url

CHAT_MODEL=your_chat_model
EMBEDDING_MODEL=your_embedding_model
EMBEDDING_DIMENSIONS=768

VECTOR_TABLE=rag_chunks
PDF_FOLDER=pdfs
```

Do not commit `.env`.

## Setup

### Backend

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Frontend

```bash
cd frontend
npm install
cd ..
```

### Database

Enable pgvector:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

Create the vector table:

```bash
python -m scripts.setup_db
```

Load the PDF documents:

```bash
python -m scripts.ingest
```

## Run Locally

Start FastAPI:

```bash
uvicorn app.api:app --reload --host 0.0.0.0 --port 8001
```

Start React:

```bash
cd frontend
npm run dev
```

Frontend: `http://localhost:5173`

Backend: `http://localhost:8001`

## API

```text
GET  /health
POST /predict
POST /ask
```

## Deployment

```text
GitHub
 ↓
Render
 ↓
Docker
 ↓
FastAPI + React
 ↓
Neon PostgreSQL + pgvector
```

## Disclaimer

This project is for **educational purposes only**. The prediction result is not a medical diagnosis and should not be used for clinical decisions.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
