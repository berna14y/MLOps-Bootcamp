from fastapi import FastAPI, HTTPException, Request, Depends
from sqlmodel import Session
from models import Churn, CreateUpdateChurn
import joblib
import pandas as pd
from database import engine, get_db, create_db_and_tables

# Load the pipeline
pipeline = joblib.load("saved_models/churn_prediction_pipeline.pkl")

app = FastAPI()

# Creates all the tables defined in models module
create_db_and_tables()


def insert_churn_record(request, prediction, client_ip, db):
    new_churn = Churn(
        CustomerId=request["CustomerId"],
        CreditScore=request["CreditScore"],
        Geography=request["Geography"],
        Gender=request["Gender"],
        Age=request["Age"],
        Tenure=request["Tenure"],
        Balance=request["Balance"],
        NumOfProducts=request["NumOfProducts"],
        HasCrCard=request["HasCrCard"],
        IsActiveMember=request["IsActiveMember"],
        EstimatedSalary=request["EstimatedSalary"],
        prediction=prediction,
        client_ip=client_ip
    )

    with db as session:
        session.add(new_churn)
        session.commit()
        session.refresh(new_churn)
    return new_churn

def make_churn_prediction(model, request):
    try:
        # Make an input vector with the correct order of features
        customer_data = {
            "CustomerId": [request["CustomerId"]],
            "CreditScore": [request["CreditScore"]],
            "Geography": [request["Geography"]],
            "Gender": [request["Gender"]],
            "Age": [request["Age"]],
            "Tenure": [request["Tenure"]],
            "Balance": [request["Balance"]],
            "NumOfProducts": [request["NumOfProducts"]],
            "HasCrCard": [request["HasCrCard"]],
            "IsActiveMember": [request["IsActiveMember"]],
            "EstimatedSalary": [request["EstimatedSalary"]]
        }
        customer_df = pd.DataFrame(customer_data)
        prediction = model.predict(customer_df)
        return "Yes" if prediction[0] else "No" 
    
    except KeyError as e:
        raise ValueError(f"Missing key in input data: {e}")
    
    except Exception as e:
        # Log the error for further analysis
        print(f"Error during prediction processing: {str(e)}")
        raise

# Churn Prediction endpoint
@app.post("/prediction/churn")
async def predict_churn(request: CreateUpdateChurn, fastapi_req: Request, db: Session = Depends(get_db)):
    try:
        # Make the prediction
        prediction = make_churn_prediction(pipeline, request.dict())
        # Insert the prediction record into the database
        db_insert_record = insert_churn_record(request=request.dict(), prediction=prediction,
                                               client_ip=fastapi_req.client.host, db=db)
        return {"prediction": prediction, "db_record": db_insert_record.Id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/client")
def client_info(request: Request):
    return {"client_host": request.client.host, "client_port": request.client.port}


@app.get("/")
async def root():
    return {"data": "Welcome to the Churn Prediction API"}

# pickle dosyasından okuyarak fastapi db'ye sonuçlar kaydederek sunduk



