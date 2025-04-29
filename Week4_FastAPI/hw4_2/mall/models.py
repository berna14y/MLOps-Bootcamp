# models.py
from sqlmodel import SQLModel, Field
from typing import Optional, List

class Customer(SQLModel, table=True):
    CustomerID: Optional[int] = Field(default=None, primary_key=True)
    customerFName: Optional[str] = Field(default=None)
    customerLName: Optional[str] = Field(default=None)
    customerEmail: Optional[str] = Field(default=None)
    customerPassword: str  # Hashed password
    customerStreet: Optional[str] = Field(default=None)
    customerCity: Optional[str] = Field(default=None)
    customerState: Optional[str] = Field(default=None)
    customerZipcode: Optional[str] = Field(default=None)

class CreateUpdateCustomer(SQLModel):
    customerFName: Optional[str]
    customerLName: Optional[str]
    customerEmail: Optional[str]
    customerStreet: Optional[str]
    customerCity: Optional[str]
    customerState: Optional[str]
    customerZipcode: Optional[str]

class CustomerCreate(CreateUpdateCustomer):
    customerPassword: str  # For registration (plain text)

class ShowCustomer(SQLModel):  # For API responses (no password)
    CustomerID: int
    customerFName: Optional[str]
    customerLName: Optional[str]
    customerEmail: Optional[str]
    customerStreet: Optional[str]
    customerCity: Optional[str]
    customerState: Optional[str]
    customerZipcode: Optional[str]

class CustomerCreateBatch(SQLModel):
    customers: List[CustomerCreate]