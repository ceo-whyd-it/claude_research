"""
Model Registry Demo

Demonstrates model lifecycle management:
- Registering models
- Versioning
- Stage transitions (Staging → Production)
- Loading models by stage
"""

import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pandas as pd

# Setup
X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

mlflow.set_experiment("model_registry_demo")
model_name = "iris_production_model"

print("🏷️  Model Registry Lifecycle Demo\n")

# Step 1: Train and register first version
print("1️⃣ Training and registering model version 1...")
with mlflow.start_run(run_name="version_1"):
    model = RandomForestClassifier(n_estimators=50, random_state=42)
    model.fit(X_train, y_train)
    accuracy = model.score(X_test, y_test)

    mlflow.log_param("n_estimators", 50)
    mlflow.log_metric("accuracy", accuracy)

    # Register the model
    mlflow.sklearn.log_model(
        sk_model=model,
        artifact_path="model",
        registered_model_name=model_name
    )

    print(f"   ✅ Registered '{model_name}' version 1 (accuracy: {accuracy:.3f})")

# Step 2: Train and register second version (improved)
print("\n2️⃣ Training and registering model version 2 (improved)...")
with mlflow.start_run(run_name="version_2"):
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    accuracy = model.score(X_test, y_test)

    mlflow.log_param("n_estimators", 100)
    mlflow.log_metric("accuracy", accuracy)

    mlflow.sklearn.log_model(
        sk_model=model,
        artifact_path="model",
        registered_model_name=model_name
    )

    print(f"   ✅ Registered '{model_name}' version 2 (accuracy: {accuracy:.3f})")

# Step 3: Manage model stages
print("\n3️⃣ Managing model stages...")
client = MlflowClient()

# Get latest versions
latest_versions = client.get_latest_versions(model_name)
print(f"   Found {len(latest_versions)} versions of '{model_name}'")

# Promote version 2 to Production
print("\n   Transitioning version 2 to Production...")
client.transition_model_version_stage(
    name=model_name,
    version=2,
    stage="Production",
    archive_existing_versions=True
)
print("   ✅ Version 2 is now in Production stage")

# Step 4: Load model from registry
print("\n4️⃣ Loading production model...")
model_uri = f"models:/{model_name}/Production"
loaded_model = mlflow.pyfunc.load_model(model_uri)

# Make predictions
sample_data = pd.DataFrame([X_test[0]], columns=[f"feature_{i}" for i in range(X_test.shape[1])])
prediction = loaded_model.predict(sample_data)

print(f"   ✅ Loaded production model from registry")
print(f"   Prediction: {prediction[0]}")

# Step 5: List all registered models
print("\n5️⃣ All registered models:")
for rm in client.search_registered_models():
    print(f"   📦 {rm.name}")
    for version in client.get_latest_versions(rm.name):
        print(f"      - Version {version.version}: Stage={version.current_stage}")

print("\n🎉 Model Registry Demo Complete!")
print("\n👉 In MLflow UI:")
print("   1. Go to 'Models' tab")
print("   2. Click on 'iris_production_model'")
print("   3. See version history and stage transitions")
