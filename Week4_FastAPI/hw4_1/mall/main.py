from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class AddNumbers(BaseModel):
    x: int
    y: int

@app.post("/add")
def add_numbers(numbers: AddNumbers):
    return {"result": numbers.x + numbers.y}

@app.get("/")
async def root():
    return {"message": "Welcome to the Simple Adder API!"}

