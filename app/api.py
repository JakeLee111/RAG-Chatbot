# Import FastAPI.
from fastapi import FastAPI

# Import Pydantic for JSON validation.
from pydantic import BaseModel, Field

# Import the RAG function we already tested.
from app.rag import answer_question

# Import the new ML prediction function.
from app.prediction import predict_heart_disease

# Import Path so we can find frontend/dist.
from pathlib import Path

# Let FastAPI serve built React files.
from fastapi.staticfiles import StaticFiles


# Create the web application.
app = FastAPI(
    title="RAG API",
    version="1.0.0",
)


# Define the JSON body for a question.
class AskRequest(BaseModel):
    # Require a useful question and prevent huge input.
    question: str = Field(
        min_length=2,
        max_length=2000,
    )


# Describe exactly what the React form must send.
class HeartPredictionInput(BaseModel):
    age: int = Field(ge=1, le=120)
    sex: str
    chest_pain_type: str
    resting_bp: int = Field(gt=0)
    cholesterol: int = Field(gt=0)
    fasting_bs: int = Field(ge=0, le=1)
    resting_ecg: str
    max_hr: int = Field(gt=0)
    exercise_angina: str
    oldpeak: float
    st_slope: str


# Prediction endpoint.
@app.post("/predict")
def predict(request: HeartPredictionInput):
    # Convert frontend names into dataset column names.
    patient = {
        "Age": request.age,
        "Sex": request.sex,
        "ChestPainType": request.chest_pain_type,
        "RestingBP": request.resting_bp,
        "Cholesterol": request.cholesterol,
        "FastingBS": request.fasting_bs,
        "RestingECG": request.resting_ecg,
        "MaxHR": request.max_hr,
        "ExerciseAngina": request.exercise_angina,
        "Oldpeak": request.oldpeak,
        "ST_Slope": request.st_slope,
    }

    # Run the saved XGBoost model.
    return predict_heart_disease(patient)


# Health endpoint.
@app.get("/health")
def health():
    return {
        "status": "ok"
    }


# Chatbot endpoint.
@app.post("/ask")
def ask(request: AskRequest):
    return answer_question(
        request.question.strip()
    )


# Find the React production build folder.
FRONTEND_DIST = (
    Path(__file__).resolve().parent.parent
    / "frontend"
    / "dist"
)


# Serve React only if npm run build created frontend/dist.
if FRONTEND_DIST.exists():
    app.mount(
        "/",
        StaticFiles(
            directory=FRONTEND_DIST,
            html=True,
        ),
        name="frontend",
    )