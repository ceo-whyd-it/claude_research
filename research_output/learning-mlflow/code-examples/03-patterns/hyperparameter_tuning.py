"""
Hyperparameter Tuning with MLflow

Demonstrates systematic hyperparameter search with nested runs.
"""

import mlflow
import mlflow.sklearn
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from itertools import product

# Set experiment
mlflow.set_experiment("wine_hyperparameter_tuning")

# Load data
print("Loading data...")
X, y = load_wine(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define hyperparameter grid
n_estimators_options = [50, 100, 200]
max_depth_options = [5, 10, 20]
min_samples_split_options = [2, 5, 10]

total_combinations = len(n_estimators_options) * len(max_depth_options) * len(min_samples_split_options)
print(f"Testing {total_combinations} hyperparameter combinations...\n")

# Create a parent run for the tuning session
with mlflow.start_run(run_name="hyperparameter_tuning_session") as parent_run:

    best_accuracy = 0
    best_params = {}
    run_number = 0

    # Try all combinations
    for n_est, max_d, min_split in product(
        n_estimators_options, max_depth_options, min_samples_split_options
    ):
        run_number += 1

        # Create a child run for each hyperparameter combination
        with mlflow.start_run(
            run_name=f"run_{run_number:02d}_n{n_est}_d{max_d}_s{min_split}",
            nested=True
        ):
            # Train model
            model = RandomForestClassifier(
                n_estimators=n_est,
                max_depth=max_d,
                min_samples_split=min_split,
                random_state=42
            )
            model.fit(X_train, y_train)

            # Evaluate
            predictions = model.predict(X_test)
            accuracy = accuracy_score(y_test, predictions)

            # Log parameters and metrics
            mlflow.log_param("n_estimators", n_est)
            mlflow.log_param("max_depth", max_d)
            mlflow.log_param("min_samples_split", min_split)
            mlflow.log_metric("accuracy", accuracy)

            # Track best model
            if accuracy > best_accuracy:
                best_accuracy = accuracy
                best_params = {
                    "n_estimators": n_est,
                    "max_depth": max_d,
                    "min_samples_split": min_split
                }

                # Log the best model
                mlflow.sklearn.log_model(model, "best_model")

            print(f"[{run_number:2d}/{total_combinations}] "
                  f"n_est={n_est:3d}, max_d={max_d:2d}, min_split={min_split:2d} "
                  f"→ accuracy={accuracy:.3f} {'🏆' if accuracy == best_accuracy else ''}")

    # Log best results to parent run
    mlflow.log_params(best_params)
    mlflow.log_metric("best_accuracy", best_accuracy)

    print(f"\n{'='*60}")
    print(f"🏆 Best Accuracy: {best_accuracy:.3f}")
    print(f"🏆 Best Parameters:")
    for param, value in best_params.items():
        print(f"   - {param}: {value}")
    print(f"{'='*60}")

print("\n👉 View results in MLflow UI:")
print("   - Parent run shows best parameters and accuracy")
print("   - Child runs show all hyperparameter combinations")
print("   - Use 'Compare' to analyze parameter impact")
