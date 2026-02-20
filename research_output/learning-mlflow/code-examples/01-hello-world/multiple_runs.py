"""
Multiple MLflow Runs Example

Demonstrates how to track multiple experiments and compare them.
"""

import mlflow

print("Running multiple experiments with different learning rates...\n")

# Run 3 experiments with different learning rates
for lr in [0.001, 0.01, 0.1]:
    with mlflow.start_run():
        mlflow.log_param("learning_rate", lr)

        # Simulate accuracy (higher LR = lower accuracy in this toy example)
        accuracy = 0.95 - (lr * 2)
        mlflow.log_metric("accuracy", accuracy)

        print(f"Run with lr={lr}: accuracy={accuracy:.3f}")

print("\n✅ All runs complete!")
print("👉 Open MLflow UI and click 'Compare' to see differences")
print("   You can sort by accuracy to find the best learning rate")
