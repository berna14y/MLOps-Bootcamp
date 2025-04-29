from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from fastapi import FastAPI, Response

class Customer(BaseModel):
    CustomerID: int
    Gender: Optional[str] = None
    Age: Optional[int] = None
    customerCity: Optional[str] = None


app = FastAPI()

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(content=None, status_code=204)


@app.post("/customers")
async def create_customer(customer: Customer):
    return {"data": f"Customer {customer.CustomerID} is created."}
