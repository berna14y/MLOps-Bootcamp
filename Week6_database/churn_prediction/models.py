from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field

class Churn(SQLModel, table=True):
    Id: Optional[int] = Field(default=None, primary_key=True)
    CustomerId: int
    CreditScore: int
    Geography: str
    Gender: str
    Age: int
    Tenure: int
    Balance: float
    NumOfProducts: int
    HasCrCard: int
    IsActiveMember: int
    EstimatedSalary: float
    prediction: str
    prediction_time: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    client_ip: str

class CreateUpdateChurn(SQLModel):
    CustomerId: int
    CreditScore: int
    Geography: str
    Gender: str
    Age: int
    Tenure: int
    Balance: float
    NumOfProducts: int
    HasCrCard: int
    IsActiveMember: int
    EstimatedSalary: float

    class Config:
        schema_extra = {
            "example": {
                "CustomerId": 15634602,
                "CreditScore": 619,
                "Geography": "France",
                "Gender": "Female",
                "Age": 42,
                "Tenure": 2,
                "Balance": 0.0,
                "NumOfProducts": 1,
                "HasCrCard": 1,
                "IsActiveMember": 1,
                "EstimatedSalary": 101348.88
            }
        }

