"""
Experiments Demo

Shows how to organize runs into experiments for better organization.
"""

import mlflow
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Load data
X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

print("Demonstrating experiment organization...\n")

# Experiment 1: Random Forest Tuning
print("📂 Experiment 1: Random Forest Tuning")
mlflow.set_experiment("iris_random_forest")

for n_estimators in [10, 50, 100]:
    with mlflow.start_run(run_name=f"rf_n{n_estimators}"):
        model = RandomForestClassifier(n_estimators=n_estimators, random_state=42)
        model.fit(X_train, y_train)
        accuracy = accuracy_score(y_test, model.predict(X_test))

        mlflow.log_param("n_estimators", n_estimators)
        mlflow.log_metric("accuracy", accuracy)

        print(f"   n_estimators={n_estimators} → accuracy={accuracy:.3f}")

# Experiment 2: Logistic Regression Tuning
print("\n📂 Experiment 2: Logistic Regression Tuning")
mlflow.set_experiment("iris_logistic_regression")

for C in [0.1, 1.0, 10.0]:
    with mlflow.start_run(run_name=f"lr_C{C}"):
        model = LogisticRegression(C=C, max_iter=1000, random_state=42)
        model.fit(X_train, y_train)
        accuracy = accuracy_score(y_test, model.predict(X_test))

        mlflow.log_param("C", C)
        mlflow.log_metric("accuracy", accuracy)

        print(f"   C={C} → accuracy={accuracy:.3f}")

print("\n✅ Created 2 experiments with 6 total runs")
print("👉 In MLflow UI, you'll see:")
print("   - 'iris_random_forest' experiment with 3 runs")
print("   - 'iris_logistic_regression' experiment with 3 runs")
print("   This keeps related runs organized and easy to find!")
