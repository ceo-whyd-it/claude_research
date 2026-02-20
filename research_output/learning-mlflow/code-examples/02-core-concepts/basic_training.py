"""
Basic Training Script with MLflow Tracking

Demonstrates a complete training workflow with:
- Experiment setup
- Autologging
- Custom metric logging
- Model registration
"""

import mlflow
import mlflow.sklearn
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, precision_score

# Set experiment name
mlflow.set_experiment("wine_classification")

# Load data
print("Loading wine dataset...")
X, y = load_wine(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"Training set: {len(X_train)} samples")
print(f"Test set: {len(X_test)} samples\n")

# Enable autologging (captures parameters automatically)
mlflow.sklearn.autolog()

# Train model
print("Training Random Forest model...")
with mlflow.start_run(run_name="random_forest_baseline"):
    # Define model
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42
    )

    # Train
    model.fit(X_train, y_train)

    # Evaluate
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    f1 = f1_score(y_test, predictions, average='weighted')
    precision = precision_score(y_test, predictions, average='weighted')

    # Log additional custom metrics (beyond what autologging captures)
    mlflow.log_metric("test_accuracy", accuracy)
    mlflow.log_metric("test_f1", f1)
    mlflow.log_metric("test_precision", precision)

    # Log model to registry
    mlflow.sklearn.log_model(
        sk_model=model,
        artifact_path="model",
        registered_model_name="wine_classifier"
    )

    print(f"✅ Model trained and logged!")
    print(f"   Test Accuracy: {accuracy:.3f}")
    print(f"   Test F1 Score: {f1:.3f}")
    print(f"   Test Precision: {precision:.3f}")

print("\n👉 View results in MLflow UI:")
print("   1. Run: mlflow ui")
print("   2. Open: http://127.0.0.1:5000")
print("   3. Navigate to 'wine_classification' experiment")
