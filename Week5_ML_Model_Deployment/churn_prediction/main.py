from fastapi import FastAPI, HTTPException
from models import Churn
import joblib
import pandas as pd

(loaded_model, loaded_feature_names) = joblib.load("saved_models/churn_model_with_features.pkl")

app = FastAPI()

@app.post("/prediction/churn")
async def predict_churn(request: Churn):
    try:
        input_data = pd.DataFrame([request.dict()])  # Convert AFTER validation
        input_data = input_data[loaded_feature_names]
        prediction = loaded_model.predict(input_data)[0]
        return {"prediction": int(prediction)}
    except Exception as e:
        # Log the error for debugging
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
