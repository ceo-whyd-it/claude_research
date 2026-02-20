"""
Model Comparison with MLflow

Compare multiple ML algorithms systematically and find the best one.
"""

import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
import pandas as pd

# Setup
mlflow.set_experiment("model_comparison")

print("🔬 Model Comparison Experiment\n")

# Load data
X, y = load_wine(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Define models to compare
models = {
    "random_forest": RandomForestClassifier(n_estimators=100, random_state=42),
    "gradient_boosting": GradientBoostingClassifier(n_estimators=100, random_state=42),
    "logistic_regression": LogisticRegression(max_iter=1000, random_state=42),
    "svm": SVC(kernel='rbf', random_state=42)
}

results = []

# Train and evaluate each model
for model_name, model in models.items():
    print(f"Training {model_name}...")

    with mlflow.start_run(run_name=model_name):
        # Train
        model.fit(X_train, y_train)

        # Evaluate
        predictions = model.predict(X_test)

        metrics = {
            "accuracy": accuracy_score(y_test, predictions),
            "f1_score": f1_score(y_test, predictions, average='weighted'),
            "precision": precision_score(y_test, predictions, average='weighted'),
            "recall": recall_score(y_test, predictions, average='weighted')
        }

        # Log all metrics
        for metric_name, metric_value in metrics.items():
            mlflow.log_metric(metric_name, metric_value)

        mlflow.log_param("model_type", model_name)

        # Log the model
        mlflow.sklearn.log_model(model, "model")

        # Save results
        results.append({
            "model": model_name,
            **metrics
        })

        print(f"  ✅ {model_name}: accuracy={metrics['accuracy']:.3f}, "
              f"f1={metrics['f1_score']:.3f}\n")

# Create comparison DataFrame
print("="*70)
comparison_df = pd.DataFrame(results).sort_values("accuracy", ascending=False)
print("📊 Model Comparison Results:\n")
print(comparison_df.to_string(index=False))
print("="*70)

# Query best model programmatically using MLflow API
print("\n🔍 Querying best model via MLflow API...")
client = MlflowClient()
experiment = client.get_experiment_by_name("model_comparison")

runs = client.search_runs(
    experiment_ids=[experiment.experiment_id],
    order_by=["metrics.accuracy DESC"],
    max_results=1
)

if runs:
    best_run = runs[0]
    print(f"\n🏆 Best Model: {best_run.data.params['model_type']}")
    print(f"   Accuracy: {best_run.data.metrics['accuracy']:.4f}")
    print(f"   F1 Score: {best_run.data.metrics['f1_score']:.4f}")
    print(f"   Precision: {best_run.data.metrics['precision']:.4f}")
    print(f"   Recall: {best_run.data.metrics['recall']:.4f}")
    print(f"   Run ID: {best_run.info.run_id}")

print("\n👉 In MLflow UI:")
print("   - Select all 4 runs")
print("   - Click 'Compare' button")
print("   - View metrics side-by-side in charts")
