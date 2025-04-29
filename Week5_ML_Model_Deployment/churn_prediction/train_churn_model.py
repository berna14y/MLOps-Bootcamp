import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

# Load the dataset 
url = "https://raw.githubusercontent.com/erkansirin78/datasets/master/Churn_Modelling.csv" 
data = pd.read_csv(url)

# Data preprocessing
data = pd.get_dummies(data, columns=['Geography', 'Gender'])
data.drop('CustomerId', axis=1, inplace=True)
data.drop('Surname', axis=1, inplace=True)
data.drop('RowNumber', axis=1, inplace=True)

# Define features and target variable
X = data.drop('Exited', axis=1)
y = data['Exited']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# fill NaN annd infinite
X_train = X_train.fillna(0)
X_test = X_test.fillna(0)

# Train the model
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy}")
print(classification_report(y_test, y_pred))

# Save the model and feature names (in the same file, as a tuple)
feature_names = X_train.columns.tolist()  # Get feature names
joblib.dump((model, feature_names), "saved_models/churn_model_with_features.pkl")

# --- Model loading and testing section ---

# Load the model and feature names
(loaded_model, loaded_feature_names) = joblib.load("saved_models/churn_model_with_features.pkl")

# Example customer data (as a dictionary) - PAY ATTENTION TO ONE-HOT ENCODING!
example_customer_dict = {
  "CreditScore": 600,
  "Age": 30,
  "Tenure": 5,
  "Balance": 100000.0,
  "NumOfProducts": 2,
  "HasCrCard": 1,
  "IsActiveMember": 1,
  "EstimatedSalary": 50000.0,
  "Geography_France": 1,
  "Geography_Germany": 0,
  "Geography_Spain": 0,
  "Gender_Female": 1,
  "Gender_Male": 0
}

# Create DataFrame and put feature names in the correct order
example_customer = pd.DataFrame([example_customer_dict])
example_customer = example_customer[loaded_feature_names]  # Important: Keep the order

prediction = loaded_model.predict(example_customer)
print(f"Example Customer Prediction: {prediction}")