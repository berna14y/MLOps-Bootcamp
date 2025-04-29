from fastapi import FastAPI, status, Depends, HTTPException
from mall.models import Customer, CreateUpdateCustomer, ShowCustomer, CustomerCreate, CustomerCreateBatch
from mall.database import get_db, engine
from sqlmodel import Session, SQLModel, select
from passlib.context import CryptContext
from typing import List  # Import List
from sqlalchemy.exc import IntegrityError

app = FastAPI()

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

@app.on_event("startup")
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

@app.post("/customers/batch", status_code=status.HTTP_201_CREATED)
async def create_customers_batch(request: CustomerCreateBatch, session: Session = Depends(get_db)):
    created_customers = []
    try:
        with session:
            for customer_data in request.customers:
                hashed_password = hash_password(customer_data.customerPassword)
                new_customer = Customer(
                    customerFName=customer_data.customerFName,
                    customerLName=customer_data.customerLName,
                    customerEmail=customer_data.customerEmail,
                    customerPassword=hashed_password,
                    customerStreet=customer_data.customerStreet,
                    customerCity=customer_data.customerCity,
                    customerState=customer_data.customerState,
                    customerZipcode=customer_data.customerZipcode
                )
                session.add(new_customer)
                created_customers.append(new_customer)  # Append before commit

            session.commit()  # Commit outside the loop for efficiency

            for customer in created_customers:  # Refresh after commit to get CustomerID
                session.refresh(customer)

            return created_customers  # Return the list of created customers (with CustomerIDs)

    except IntegrityError as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Integrity Error: {e}")
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred: {e}")


@app.post("/customers", status_code=status.HTTP_201_CREATED)
async def create_customer(request: CustomerCreate, session: Session = Depends(get_db)):
    hashed_password = hash_password(request.customerPassword)
    new_customer = Customer(
        customerFName=request.customerFName,
        customerLName=request.customerLName,
        customerEmail=request.customerEmail,
        customerPassword=hashed_password,
        customerStreet=request.customerStreet,
        customerCity=request.customerCity,
        customerState=request.customerState,
        customerZipcode=request.customerZipcode
    )
    try:
        with session:
            session.add(new_customer)
            session.commit()
            session.refresh(new_customer)  # Refresh to get the CustomerID
            return new_customer  # Return the created customer (with CustomerID)
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred: {e}")
    
    
@app.get("/customers/{id}", status_code=status.HTTP_200_OK, response_model=ShowCustomer)
async def get_by_id(id: int, session: Session = Depends(get_db)):
    try:
        with session:
            customer = session.get(Customer, id)
            if not customer:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Customer {id} has not found.")
            return customer
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred: {e}")

@app.delete("/customer/{id}", status_code=status.HTTP_200_OK)
async def delete_customer(id: int, session: Session = Depends(get_db)):
    try:
        with session:
            customer = session.get(Customer, id)
            if not customer:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail=f"Customer with {id} has not found.")
            session.delete(customer)
            session.commit()
            return {"message": f"Customer: {id} deleted."}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred: {e}")

@app.put("/customer/{id}", status_code=status.HTTP_202_ACCEPTED)  # Update endpoint
async def update_customer(id: int, request: CreateUpdateCustomer, session: Session = Depends(get_db)):
    try:
        with session:
            customer = session.get(Customer, id)
            if not customer:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Customer with {id} has not found.")

            update_data = request.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(customer, key, value)  # Update all provided fields

            session.add(customer)
            session.commit()
            session.refresh(customer)
            return customer
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred: {e}")

@app.put("/customer/{id}/password", status_code=status.HTTP_202_ACCEPTED)
async def update_customer_password(id: int, new_password: str, session: Session = Depends(get_db)):
    try:
        with session:
            customer = session.get(Customer, id)
            if not customer:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Customer with {id} not found.")

            hashed_password = hash_password(new_password)
            customer.customerPassword = hashed_password

            session.add(customer)
            session.commit()
            session.refresh(customer)
            return {"message": "Password updated successfully"}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred: {e}")