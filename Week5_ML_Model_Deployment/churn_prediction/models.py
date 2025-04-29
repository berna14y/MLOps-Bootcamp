from pydantic import BaseModel

class Churn(BaseModel):
    CreditScore: int
    Age: int
    Tenure: int
    Balance: float  # Note: float here!
    NumOfProducts: int
    HasCrCard: int
    IsActiveMember: int
    EstimatedSalary: float  # Note: float here!
    Geography_France: int
    Geography_Germany: int
    Geography_Spain: int
    Gender_Female: int
    Gender_Male: int

    class Config:
        json_schema_extra = {
            "example": {
                "CreditScore": 600,
                "Age": 30,
                "Tenure": 5,
                "Balance": 100000.0,  # Use float in example
                "NumOfProducts": 2,
                "HasCrCard": 1,
                "IsActiveMember": 1,
                "EstimatedSalary": 50000.0,  # Use float in example
                "Geography_France": 1,
                "Geography_Germany": 0,
                "Geography_Spain": 0,
                "Gender_Female": 1,
                "Gender_Male": 0
            }
        }