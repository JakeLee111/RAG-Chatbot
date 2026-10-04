# Heart Health Assistant

A full-stack AI web app that combines:

- Heart disease prediction
- A RAG chatbot
- React frontend
- FastAPI backend
- PostgreSQL + pgvector
- Gemini
- Hugging Face deployment

> This project is for learning and portfolio use only. It is not a medical diagnosis tool and should not be used for clinical decisions.

---

## Project Overview

The app has two main features:

1. **Heart Disease Prediction**
   - The user enters health information.
   - The trained machine learning model predicts heart disease risk.
   - The model was trained separately in Jupyter Notebook.

2. **RAG Chatbot**
   - The user asks questions.
   - The chatbot searches the project knowledge base.
   - PostgreSQL + pgvector stores document embeddings.
   - Gemini generates the final answer using the retrieved context.

---

## Architecture

```text
User
 |
 v
React Frontend
 |
 +----------------------+
 |                      |
 v                      v
Heart Prediction      Chatbot
 |                      |
 v                      v
POST /predict         POST /ask
 |                      |
 +----------+-----------+
            |
            v
        FastAPI
       app/api.py
        /       \
       /         \
      v           v
Prediction      RAG
Service         Service
      |           |
      v           v
heart_model    PostgreSQL
.joblib        + pgvector
                  |
                  v
                Gemini
```

---

## Project Structure

```text
rag_chatbot/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── vector_store.py
│   ├── rag.py
│   ├── prediction.py
│   └── api.py
│
├── frontend/
│   ├── src/
│   ├── package.json
│   └── ...
│
├── models/
│   └── heart_model.joblib
│
├── scripts/
│   ├── setup_db.py
│   └── ingest.py
│
├── pdfs/
│
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env
└── README.md
```

---

## How the Prediction Model Connects

The prediction model is trained in the separate heart disease project using Jupyter Notebook.

```text
Jupyter Notebook
      |
      v
Train model
      |
      v
Save trained model
      |
      v
heart_model.joblib
      |
      v
Copy into this project
      |
      v
models/heart_model.joblib
```

Example export from the training notebook:

```python
import joblib

joblib.dump(model, "heart_model.joblib")
```

The web app then loads the saved model:

```python
import joblib

model = joblib.load("models/heart_model.joblib")
```

The web app does not connect directly to the Jupyter Notebook.

---

## Prediction Inputs

The user must provide all required values during live prediction.

Example inputs:

- Age
- Sex
- Chest Pain Type
- Resting Blood Pressure
- Cholesterol
- Fasting Blood Sugar
- Resting ECG
- Maximum Heart Rate
- Exercise Angina
- Oldpeak
- ST Slope

For live prediction, the user must provide the cholesterol value.

The training dataset may use its own offline data-cleaning process before model training.

---

## RAG Flow

```text
PDF documents
     |
     v
Load and split
     |
     v
Create embeddings
     |
     v
PostgreSQL + pgvector
     |
     v
User question
     |
     v
Retrieve related chunks
     |
     v
Gemini
     |
     v
Final answer
```

---

## Main Backend Files

### `app/config.py`

Stores project configuration such as:

- Database URL
- Gemini model
- Embedding model
- Vector table
- PDF folder

### `app/vector_store.py`

Connects LangChain to PostgreSQL + pgvector.

### `app/rag.py`

Handles:

- document retrieval
- prompt creation
- Gemini response
- source information

### `app/prediction.py`

Handles:

- loading `heart_model.joblib`
- preparing user input
- running the prediction
- returning the prediction result

### `app/api.py`

Main FastAPI application.

It exposes both chatbot and prediction endpoints.

---

## API Endpoints

### Health Check

```http
GET /health
```

Example response:

```json
{
  "status": "ok"
}
```

### Heart Disease Prediction

```http
POST /predict
```

Example request:

```json
{
  "age": 52,
  "sex": "M",
  "chest_pain_type": "ATA",
  "resting_bp": 130,
  "cholesterol": 220,
  "fasting_bs": 0,
  "resting_ecg": "Normal",
  "max_hr": 160,
  "exercise_angina": "N",
  "oldpeak": 1.0,
  "st_slope": "Up"
}
```

Example response:

```json
{
  "prediction": 0,
  "probability": 0.21
}
```

### Chatbot

```http
POST /ask
```

Example request:

```json
{
  "question": "What is cholesterol?"
}
```

---

## Local Setup

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd rag_chatbot
```

### 2. Create a Python virtual environment

```bash
python -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 4. Install frontend dependencies

```bash
cd frontend
npm install
cd ..
```

---

## Environment Variables

Create a `.env` file in the project root.

Example:

```env
GOOGLE_API_KEY=your_google_api_key

DATABASE_URL=postgresql+psycopg://rag:your_password@localhost:5432/rag

CHAT_MODEL=gemini-3.5-flash
EMBEDDING_MODEL=gemini-embedding-2
EMBEDDING_DIMENSIONS=768

VECTOR_TABLE=rag_chunks
PDF_FOLDER=pdfs
```

Do not commit `.env` to GitHub.

---

## Start PostgreSQL + pgvector

```bash
docker compose up -d
```

Check the database:

```bash
docker compose ps
```

---

## Create the Vector Table

Run:

```bash
python -m scripts.setup_db
```

This creates the PostgreSQL table used for vector storage.

---

## Ingest Documents

Put PDF files inside:

```text
pdfs/
```

Then run:

```bash
python -m scripts.ingest
```

This will:

1. Load the PDFs
2. Split them into chunks
3. Create embeddings
4. Store them in PostgreSQL + pgvector

---

## Run the FastAPI Backend

```bash
uvicorn app.api:app --reload --host 0.0.0.0 --port 8000
```

Open:

```text
http://localhost:8000/docs
```

Use the FastAPI docs page to test the endpoints.

---

## Run the React Frontend

Open another terminal:

```bash
cd frontend
npm run dev
```

The frontend will normally run on a local Vite URL such as:

```text
http://localhost:5173
```

The React app calls the FastAPI backend for:

- prediction
- chatbot requests

---

## Production Build

Build the React frontend:

```bash
cd frontend
npm run build
```

This creates the production frontend files.

FastAPI can then serve the built React files from the same application.

---

## Docker Deployment

The production Docker setup contains:

- React production build
- FastAPI backend
- Heart prediction model
- RAG application

The deployed app uses one public web server.

PostgreSQL + pgvector should remain external for production deployment.

---

## Hugging Face Deployment

The project can be deployed using a Hugging Face Docker Space.

High-level flow:

```text
GitHub / Hugging Face Space repo
        |
        v
Docker build
        |
        v
React + FastAPI
        |
        +------> heart_model.joblib
        |
        +------> Gemini API
        |
        +------> External PostgreSQL + pgvector
```

The app should listen on the Hugging Face Space port:

```text
7860
```

Store secrets such as these in Hugging Face Space settings:

- `GOOGLE_API_KEY`
- `DATABASE_URL`

Do not put production secrets directly inside the repository.

---

## Development Workflow

### Update the ML model

1. Train or improve the model in the Heart Disease Prediction project.
2. Export the trained model using `joblib`.
3. Copy the new model file into:

```text
models/heart_model.joblib
```

4. Restart the backend.
5. Test `/predict`.

### Update the RAG knowledge base

1. Add or update PDFs in `pdfs/`.
2. Run:

```bash
python -m scripts.ingest
```

3. Test `/ask`.

---

## Important Separation

The two systems have different responsibilities.

### Prediction Model

Answers:

> Based on these input values, what does the trained ML model predict?

### RAG Chatbot

Answers:

> What information can be found in the project's knowledge documents?

The chatbot should not replace the prediction model.

---

## Disclaimer

This project is for educational, research, and portfolio purposes only.

The heart disease prediction result is generated by a machine learning model and is not a medical diagnosis.

Do not use this application as a substitute for professional medical advice, diagnosis, or treatment.
