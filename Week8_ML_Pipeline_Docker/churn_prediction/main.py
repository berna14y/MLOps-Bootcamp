from fastapi import FastAPI, Request
from pydantic import BaseModel
import os
from mlflow.sklearn import load_model
import pandas as pd

# Set MLflow tracking and artifact server URIs
os.environ['MLFLOW_TRACKING_URI'] = 'http://localhost:5001/'
os.environ['MLFLOW_S3_ENDPOINT_URL'] = 'http://localhost:9000/'

# Load the model from MLflow Model Registry
model_name = "ChurnPredictionRFModel"
model_version = 1  # Replace with the version you want to use
model = load_model(
    model_uri=f"models:/{model_name}/{model_version}"
)

# Define FastAPI app
app = FastAPI()

# Define input schema using Pydantic
class ChurnRequest(BaseModel):
    CustomerId: int
    CreditScore: float
    Age: float
    Tenure: float
    Balance: float
    NumOfProducts: float
    HasCrCard: float
    IsActiveMember: float
    EstimatedSalary: float
    Geography: str
    Gender: str

# Function to make predictions
def make_churn_prediction(model, request):
    # Parse input from request
    input_data = [
        request["CreditScore"],
        request["Age"],
        request["Tenure"],
        request["Balance"],
        request["NumOfProducts"],
        request["HasCrCard"],
        request["IsActiveMember"],
        request["EstimatedSalary"],
        request["Geography"],
        request["Gender"],
    ]

    # Convert input data into a DataFrame (to match the model's preprocessing pipeline)
    input_df = pd.DataFrame([input_data], columns=[
        "CreditScore", "Age", "Tenure", "Balance", "NumOfProducts", 
        "HasCrCard", "IsActiveMember", "EstimatedSalary", "Geography", "Gender"
    ])

    # Predict
    prediction = model.predict(input_df)

    # Return prediction (0 for no churn, 1 for churn)
    return int(prediction[0])

# Churn Prediction endpoint
@app.post("/prediction/churn")
async def predict_churn(request: ChurnRequest):
    # Convert Pydantic model to dictionary
    request_dict = request.dict()

    # Extract CustomerId (for reference, not used in prediction)
    customer_id = request_dict["CustomerId"]

    # Make prediction
    prediction = make_churn_prediction(model, request_dict)

    # Return prediction along with CustomerId
    return {
        "CustomerId": customer_id,
        "prediction": prediction
    }

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Churn Prediction API"}



# Modeller MLFlow'a gönderildi oradan alıp okuyoruz artık.
# Modeli MLFlow'dan okuduk sonra FastAPI'dan sunduk.
# DB olmadan pickle dosyasından okuyarak fastapi sunduk.



