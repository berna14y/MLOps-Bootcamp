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
    prediction_time: datetime = Field(default_factory=datetime.utcnow)
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
