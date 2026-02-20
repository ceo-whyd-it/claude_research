"""
Production Model Deployment

Complete workflow from training to deployment:
1. Train a model
2. Register it
3. Promote to Production
4. Load and use for predictions
"""

import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pandas as pd
import numpy as np

# Configuration
MODEL_NAME = "production_wine_classifier"
mlflow.set_experiment("production_deployment")

print("🚀 Production Deployment Workflow\n")

# Step 1: Train and Register Model
print("1️⃣ Training and registering model...")
X, y = load_wine(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

with mlflow.start_run(run_name="production_candidate") as run:
    # Train model
    model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
    model.fit(X_train, y_train)

    # Evaluate
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)

    # Log metrics and parameters
    mlflow.log_param("n_estimators", 100)
    mlflow.log_param("max_depth", 10)
    mlflow.log_metric("accuracy", accuracy)

    # Register model
    model_info = mlflow.sklearn.log_model(
        sk_model=model,
        artifact_path="model",
        registered_model_name=MODEL_NAME
    )

    run_id = run.info.run_id
    print(f"   ✅ Model registered: {MODEL_NAME}")
    print(f"   Accuracy: {accuracy:.3f}")
    print(f"   Run ID: {run_id}\n")

# Step 2: Promote to Production
print("2️⃣ Promoting model to Production stage...")
client = MlflowClient()

# Get the latest version
latest_versions = client.get_latest_versions(MODEL_NAME, stages=["None"])

if latest_versions:
    latest_version = latest_versions[0]

    # Transition to Production
    client.transition_model_version_stage(
        name=MODEL_NAME,
        version=latest_version.version,
        stage="Production",
        archive_existing_versions=True
    )

    print(f"   ✅ Version {latest_version.version} promoted to Production\n")
else:
    print("   ❌ No model version found to promote\n")

# Step 3: Load Production Model
print("3️⃣ Loading production model...")
model_uri = f"models:/{MODEL_NAME}/Production"
production_model = mlflow.pyfunc.load_model(model_uri)
print(f"   ✅ Loaded model from: {model_uri}\n")

# Step 4: Make Predictions
print("4️⃣ Making predictions with production model...")

# Create sample input (first 5 test samples)
sample_input = pd.DataFrame(
    X_test[:5],
    columns=[f"feature_{i}" for i in range(X_test.shape[1])]
)

predictions = production_model.predict(sample_input)
actual = y_test[:5]

print("   Sample Predictions:")
print("   " + "="*50)
for i, (pred, true) in enumerate(zip(predictions, actual)):
    match = "✓" if pred == true else "✗"
    print(f"   Sample {i+1}: Predicted={int(pred)}, Actual={int(true)} {match}")
print("   " + "="*50 + "\n")

# Step 5: Deployment Information
print("5️⃣ Deployment Options:")
print("\n   Option A: Serve as REST API")
print("   " + "-"*50)
print(f"   $ mlflow models serve \\")
print(f"       --model-uri 'models:/{MODEL_NAME}/Production' \\")
print(f"       --port 5001 \\")
print(f"       --no-conda")
print()
print("   Then make predictions via HTTP:")
print("   " + "-"*50)
print("   import requests, json")
print("   url = 'http://127.0.0.1:5001/invocations'")
print("   data = {'inputs': [[13.2, 2.5, ...]]}  # Your features")
print("   response = requests.post(url, json=data)")
print("   predictions = response.json()")

print("\n   Option B: Deploy to Docker")
print("   " + "-"*50)
print(f"   $ mlflow models build-docker \\")
print(f"       --model-uri 'models:/{MODEL_NAME}/Production' \\")
print(f"       --name '{MODEL_NAME.replace('_', '-')}'")
print()
print(f"   $ docker run -p 5001:8080 {MODEL_NAME.replace('_', '-')}")

print("\n   Option C: Deploy to Cloud")
print("   " + "-"*50)
print("   - AWS SageMaker: mlflow sagemaker deploy")
print("   - Azure ML: mlflow azureml deploy")
print("   - GCP Vertex AI: Use AI Platform deployment")

print("\n✅ Production Deployment Workflow Complete!")
print(f"\n👉 Model '{MODEL_NAME}' version in Production is ready for serving")
