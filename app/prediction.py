# Work with a file path safely on every operating system.
from pathlib import Path
# Load the saved XGBoost artifact.
import joblib
# Build a one-row table for preprocessing.
import pandas as pd
# Find the project root: rag_chatbot/.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
# Point to the model file we copied from the ML repo.
MODEL_PATH = PROJECT_ROOT / "models" / "heart_model.joblib"
# Load the XGBoost model directly.
model = joblib.load("models/heart_model.joblib")
# Get the exact feature names used during training.
model_columns = model.get_booster().feature_names

# Predict one user's heart-disease class.
def predict_heart_disease(data: dict):
    # Convert the incoming JSON into one DataFrame row.
    row = pd.DataFrame([data])
    # One-hot encode the same categorical fields used during training.
    row = pd.get_dummies(row)
    # Add missing training columns as 0 and keep the exact training order.
    row = row.reindex(columns=model_columns, fill_value=0)
    # Predict class 0 or 1.
    prediction = int(model.predict(row)[0])
    # Ask XGBoost for the probability of class 1.
    probability = float(model.predict_proba(row)[0][1])
    # Return plain Python values that FastAPI can convert to JSON.
    return {
    "prediction": prediction,
    "probability": probability,
    }