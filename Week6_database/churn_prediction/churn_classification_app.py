import streamlit as st
import requests

# FastAPI endpoint URL
FASTAPI_URL = "http://127.0.0.1:8000/prediction/churn"

# Streamlit UI
st.title("Bank Customer Churn Prediction App")
st.write("Enter customer details below and click Predict to see if they will churn:")

# Input fields
customer_id = st.number_input("Customer ID", min_value=1, value=15634602)
credit_score = st.number_input("Credit Score", min_value=0, max_value=850, value=619)
geography = st.selectbox("Geography", ["France", "Germany", "Spain"])
gender = st.selectbox("Gender", ["Male", "Female"])
age = st.number_input("Age", min_value=18, max_value=100, value=42)
tenure = st.number_input("Tenure", min_value=0, max_value=20, value=2)
balance = st.number_input("Balance", min_value=0.0, value=0.0)
num_of_products = st.number_input("Number of Products", min_value=1, max_value=4, value=1)
has_credit_card = st.selectbox("Has Credit Card", [0, 1])
is_active_member = st.selectbox("Is Active Member", [0, 1])
estimated_salary = st.number_input("Estimated Salary", min_value=0.0, value=101348.88)

# Prediction button
if st.button("Predict"):
    # Prepare input data as JSON
    input_data = {
        "CustomerId": customer_id,
        "CreditScore": credit_score,
        "Geography": geography,
        "Gender": gender,
        "Age": age,
        "Tenure": tenure,
        "Balance": balance,
        "NumOfProducts": num_of_products,
        "HasCrCard": has_credit_card,
        "IsActiveMember": is_active_member,
        "EstimatedSalary": estimated_salary
    }

    try:
        # Send POST request to FastAPI endpoint
        response = requests.post(FASTAPI_URL, json=input_data)

        if response.status_code == 200:
            prediction = response.json()["result"]
            st.success(f"Prediction: The customer is **{'likely to churn' if prediction == 'Will leave' else 'not likely to churn'}**.")
        else:
            st.error(f"Error: Received status code {response.status_code}")

    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {e}")
