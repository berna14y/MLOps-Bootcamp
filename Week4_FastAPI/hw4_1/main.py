from fastapi import FastAPI
from pydantic import BaseModel

class AddNumbers(BaseModel):
    x: int
    y: int

app = FastAPI()

@app.post("/add")
def add_numbers(numbers: AddNumbers):
    return {"result": numbers.x + numbers.y}

@app.get("/")
def root():
    return {"message": "Welcome to the Simple Adder API!"}
