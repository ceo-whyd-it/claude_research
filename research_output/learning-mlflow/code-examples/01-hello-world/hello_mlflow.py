"""
MLflow Hello World Example

The simplest possible MLflow example - tracking one parameter and one metric.
"""

import mlflow

# Start an MLflow run
with mlflow.start_run():
    # Log a parameter (input to your experiment)
    mlflow.log_param("learning_rate", 0.01)

    # Simulate training and log a metric (output/result)
    accuracy = 0.95
    mlflow.log_metric("accuracy", accuracy)

    print(f"✅ Logged: learning_rate=0.01, accuracy={accuracy}")

print("\n🎉 Success! Your first MLflow experiment is logged.")
print("👉 Run 'mlflow ui' to view results in the web interface")
print("   Navigate to http://127.0.0.1:5000 in your browser")
