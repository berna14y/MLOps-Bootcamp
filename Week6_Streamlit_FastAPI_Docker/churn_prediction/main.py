from fastapi import FastAPI, HTTPException, Request
from models import Churn, CreateUpdateChurn
import joblib
import pandas as pd

# Load the pipeline
pipeline = joblib.load("saved_models/churn_prediction_pipeline.pkl")

app = FastAPI()

@app.post("/prediction/churn")
def predict_churn(data: CreateUpdateChurn):
    try:
        # Data conversion to DataFrame to comply with pipeline requirements
        input_df = pd.DataFrame([data.dict()])
        prediction = pipeline.predict(input_df)[0]
        churn_result = "Yes" if prediction else "No"
        return {"CustomerId": data.CustomerId, "result": churn_result}  # Changed key to "result"
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/client")
def client_info(request: Request):
    return {"client_host": request.client.host, "client_port": request.client.port}

