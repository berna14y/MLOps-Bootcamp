import os
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score
import mlflow
import mlflow.sklearn
from urllib.parse import urlparse

# Load data
df = pd.read_csv("https://raw.githubusercontent.com/erkansirin78/datasets/master/Churn_Modelling.csv")

# Select features and target
X = df.iloc[:, 3:-1]
y = df['Exited']

# Preprocessing for numerical data
numerical_transformer = StandardScaler()

# Preprocessing for categorical data
categorical_transformer = Pipeline(steps=[
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

# Bundle preprocessing for numerical and categorical data
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numerical_transformer, ['CreditScore', 'Age', 'Tenure', 'Balance', 'NumOfProducts', 'HasCrCard', 'IsActiveMember', 'EstimatedSalary']),
        ('cat', categorical_transformer, ['Geography', 'Gender'])
    ])

# Define the base model
model = RandomForestClassifier(random_state=42)

# Create a pipeline
pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                           ('classifier', model)])

# Define the parameter grid
param_grid = {
    'classifier__n_estimators': [100, 200, 300],
    'classifier__max_features': ['auto', 'sqrt', 'log2'],
    'classifier__max_depth': [None, 10, 20, 30],
    'classifier__min_samples_split': [2, 5, 10],
    'classifier__min_samples_leaf': [1, 2, 4]
}

# Setup the GridSearchCV
grid_search = GridSearchCV(estimator=pipeline, param_grid=param_grid, cv=5, scoring='accuracy', verbose=2, n_jobs=-1)

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

# Set MLflow tracking URI and experiment name
os.environ['MLFLOW_TRACKING_URI'] = 'http://localhost:5001/'
os.environ['MLFLOW_S3_ENDPOINT_URL'] = 'http://localhost:9000/'

experiment_name = "Churn Prediction with MLflow"
mlflow.set_experiment(experiment_name)

registered_model_name = "ChurnPredictionRFModel"

with mlflow.start_run(run_name="churn-rf-sklearn") as run:
    # Perform GridSearchCV
    grid_search.fit(X_train, y_train)

    # Best estimator
    best_pipeline = grid_search.best_estimator_

    # Predictions
    y_pred = best_pipeline.predict(X_test)

    # Evaluation
    accuracy = accuracy_score(y_test, y_pred)
    print("Best Parameters: ", grid_search.best_params_)
    print("Accuracy: ", accuracy)
    print("Classification Report:\n", classification_report(y_test, y_pred))

    # Log parameters and metrics
    mlflow.log_params(grid_search.best_params_)
    mlflow.log_metric("accuracy", accuracy)

    # Log the model
    tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme

    # Model registry does not work with file store
    if tracking_url_type_store != "file":
        # Register the model
        mlflow.sklearn.log_model(best_pipeline, "model", registered_model_name=registered_model_name)
    else:
        mlflow.sklearn.log_model(best_pipeline, "model")

# Optional part
# name = registered_model_name
# client = MlflowClient()
#
# model_uri = "runs:/{}/sklearn-model".format(run.info.run_id)
# print(model_uri)
#
# mv = client.create_model_version(name, model_uri, run.info.run_id)
# print("model version {} created".format(mv.version))
# last_mv = mv.version
# print(last_mv)
#
# def print_models_info(models):
#     for m in models:
#         print("name: {}".format(m.name))
#         print("latest version: {}".format(m.version))
#         print("run_id: {}".format(m.run_id))
#         print("current_stage: {}".format(m.current_stage))
#
# def get_latest_model_version(models):
#     for m in models:
#         print("name: {}".format(m.name))
#         print("latest version: {}".format(m.version))
#         print("run_id: {}".format(m.run_id))
#         print("current_stage: {}".format(m.current_stage))
#     return m.version
#
# models = client.get_latest_versions(name, stages=["None"])
# print_models_info(models)
#
# print(f"Latest version: { get_latest_model_version(models) }")