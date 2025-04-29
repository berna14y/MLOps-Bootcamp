from pydantic import BaseModel

class AddNumbers(BaseModel):
    x: int
    y: int
