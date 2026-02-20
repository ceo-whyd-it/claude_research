"""
Autologging Demo

Shows the power of autologging - minimal code, maximum tracking.
"""

import mlflow
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import xgboost as xgb

# Load data
X, y = load_diabetes(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

print("🪄 Autologging Magic Demo\n")

# Enable global autologging (works for all supported frameworks)
mlflow.autolog()

mlflow.set_experiment("autologging_demo")

# Example 1: Scikit-learn with autologging
print("1️⃣ Training scikit-learn Random Forest...")
with mlflow.start_run(run_name="sklearn_autolog"):
    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=10,
        min_samples_split=5,
        random_state=42
    )
    model.fit(X_train, y_train)
    score = model.score(X_test, y_test)

    print(f"   R² Score: {score:.3f}")
    print("   ✅ MLflow automatically logged:")
    print("      - All hyperparameters (n_estimators, max_depth, etc.)")
    print("      - Training score")
    print("      - The trained model")
    print("      - Feature importances\n")

# Example 2: XGBoost with autologging
print("2️⃣ Training XGBoost model...")
dtrain = xgb.DMatrix(X_train, label=y_train)
dtest = xgb.DMatrix(X_test, label=y_test)

params = {
    "max_depth": 6,
    "eta": 0.1,
    "objective": "reg:squarederror",
    "eval_metric": "rmse"
}

with mlflow.start_run(run_name="xgboost_autolog"):
    bst = xgb.train(
        params,
        dtrain,
        num_boost_round=100,
        evals=[(dtest, "test")],
        verbose_eval=False
    )

    print("   ✅ MLflow automatically logged:")
    print("      - All XGBoost parameters")
    print("      - Evaluation metrics (RMSE)")
    print("      - The trained booster model\n")

print("🎉 That's autologging! No manual mlflow.log_param() or mlflow.log_metric() needed!")
print("\n👉 Check MLflow UI to see everything that was logged automatically")

print("\n💡 Pro Tip: You can still combine autologging with manual logging:")
print("   mlflow.autolog()  # Automatic logging")
print("   # ... train model ...")
print("   mlflow.log_metric('custom_metric', value)  # Manual logging")
