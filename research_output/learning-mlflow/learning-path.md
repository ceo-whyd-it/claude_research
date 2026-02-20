# MLflow Learning Path

A progressive guide to mastering MLflow - from first principles to production deployment.

---

## Level 1: Overview & Motivation

### What problem does MLflow solve?

Machine learning development is inherently iterative. You experiment with different:
- **Algorithms** (Random Forest vs XGBoost vs Neural Networks)
- **Hyperparameters** (learning rate, number of layers, regularization)
- **Features** (which variables to include, how to transform them)
- **Data versions** (different training sets, preprocessing approaches)

Without proper tooling, this creates chaos:
- 📂 Notebooks scattered across directories: `model_v2_final_ACTUALLY_FINAL.ipynb`
- 🤔 Can't remember which hyperparameters produced that great result last week
- 🔍 No way to compare 50 different experiment runs systematically
- 🚀 Deploying models to production is manual and error-prone
- 👥 Teams can't collaborate - everyone has their own tracking system

**MLflow solves this by providing**:
1. **Automatic experiment tracking** - Log parameters, metrics, and artifacts without manual bookkeeping
2. **Centralized model registry** - One source of truth for all model versions
3. **Reproducible packaging** - Capture dependencies and environment for any model
4. **Flexible deployment** - Deploy to Docker, Kubernetes, AWS, Azure, GCP with standard interfaces
5. **LLM observability** - Trace and debug GenAI applications end-to-end

### What existed before? Why is MLflow better?

**Before MLflow (2018)**:
- Manual spreadsheets to track experiments
- Custom scripts to save model checkpoints
- No standard way to package models
- Deployment was framework-specific
- Every team built their own tracking infrastructure

**After MLflow**:
- Automatic tracking with `mlflow.autolog()`
- Built-in versioning and registry
- Framework-agnostic model packaging
- One-line deployment commands
- Open-source, community-driven standard

**MLflow's killer features**:
- ✅ **Framework-agnostic**: Works with scikit-learn, PyTorch, TensorFlow, XGBoost, LangChain, and 30+ frameworks
- ✅ **Open-source**: No vendor lock-in, run anywhere
- ✅ **Production-ready**: Used by Spotify, Meta, and 18,000+ companies
- ✅ **Comprehensive**: Covers entire ML lifecycle (tracking → registry → deployment)
- ✅ **Extensible**: Plugin architecture for custom integrations

### Who uses it? For what?

**Data Scientists**:
- Track hundreds of training experiments
- Compare model performance systematically
- Share results with team members

**ML Engineers**:
- Package models for deployment
- Automate model promotion pipelines
- Monitor model performance in production

**LLM/GenAI Developers**:
- Trace LLM application behavior
- Evaluate prompt quality
- Debug multi-agent systems

**MLOps Teams**:
- Centralize experiment tracking across teams
- Enforce model governance policies
- Automate CI/CD for ML models

**Industries**:
- Finance (fraud detection, risk scoring)
- Healthcare (diagnostics, treatment prediction)
- Retail (recommendations, demand forecasting)
- Manufacturing (predictive maintenance)
- Tech (search, recommendations, content moderation)

### When should you NOT use MLflow?

MLflow might not be the best fit if:

❌ **You're doing one-off analysis**
- For ad-hoc data exploration with no model deployment, MLflow adds unnecessary overhead
- Use: Jupyter notebooks + manual notes

❌ **You need extensive team collaboration features**
- MLflow lacks built-in user management, permissions, and advanced collaboration
- Consider: Weights & Biases, Neptune.ai for better team features

❌ **You want a fully managed, zero-setup solution**
- MLflow requires self-hosting (or Databricks for managed version)
- Consider: W&B, Comet.ml for cloud-hosted solutions

❌ **You need real-time experiment monitoring dashboards**
- MLflow UI is functional but basic compared to commercial tools
- Consider: TensorBoard (for deep learning), W&B (for advanced viz)

❌ **Your entire stack is on a single cloud platform**
- If you're 100% AWS, SageMaker might integrate more seamlessly
- If you're 100% Azure, Azure ML might be more native
- If you're 100% GCP, Vertex AI might be simpler

**When MLflow shines**:
- ✅ You need flexibility and no vendor lock-in
- ✅ You use multiple ML frameworks
- ✅ You want cost-effective, self-hosted infrastructure
- ✅ You're building production ML systems
- ✅ You need both traditional ML AND LLM/GenAI support

---

## Level 2: Installation & Hello World

### Prerequisites

**System Requirements**:
- Python 3.10 or higher
- pip (Python package manager)
- 100MB disk space for MLflow package
- Additional space for experiment artifacts

**Knowledge Prerequisites**:
- Basic Python programming
- Familiarity with machine learning concepts
- Understanding of model training (helpful but not required)

### Installation Steps

**Step 1: Install MLflow**

```bash
pip install mlflow
```

This installs MLflow with core dependencies. For specific integrations:

```bash
# For database backends (PostgreSQL, MySQL)
pip install mlflow[db]

# For LLM/GenAI features
pip install mlflow[genai]

# For LangChain integration
pip install mlflow[langchain]

# For all extras
pip install mlflow[extras]
```

**Step 2: Verify Installation**

```bash
mlflow --version
```

Expected output:
```
mlflow, version 3.9.0
```

**Step 3: Check Python API**

```python
import mlflow
print(f"MLflow version: {mlflow.__version__}")
```

### Minimal Working Example

Let's create the simplest possible MLflow example - tracking a single parameter and metric.

**Create a file: `hello_mlflow.py`**

```python
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
```

**Run it**:

```bash
python hello_mlflow.py
```

**Expected output**:
```
✅ Logged: learning_rate=0.01, accuracy=0.95

🎉 Success! Your first MLflow experiment is logged.
👉 Run 'mlflow ui' to view results in the web interface
```

**What just happened?**
1. MLflow created a directory `mlruns/` in your current directory
2. Inside, it stored metadata about your run (parameters, metrics, timestamps)
3. Your experiment is now tracked and queryable

### View Your Results

**Step 1: Start the MLflow UI**

```bash
mlflow ui
```

Expected output:
```
[INFO] Starting gunicorn 20.1.0
[INFO] Listening at: http://127.0.0.1:5000
```

**Step 2: Open your browser**

Navigate to: `http://127.0.0.1:5000`

You'll see:
- **Experiments tab**: Lists all experiments (you'll see "Default" experiment)
- **Your run**: Click to see parameters, metrics, and metadata
- **Timeline**: When the run started and ended
- **Artifacts**: Files logged during the run

**Step 3: Explore the UI**

- Click on your run to see details
- Notice the `learning_rate` parameter
- Notice the `accuracy` metric
- See metadata (start time, duration, source code)

### Verify It Works

**Test 1: Run multiple experiments**

```python
import mlflow

# Run 3 experiments with different learning rates
for lr in [0.001, 0.01, 0.1]:
    with mlflow.start_run():
        mlflow.log_param("learning_rate", lr)
        # Simulate accuracy (higher LR = lower accuracy in this toy example)
        accuracy = 0.95 - (lr * 2)
        mlflow.log_metric("accuracy", accuracy)
        print(f"Run with lr={lr}: accuracy={accuracy:.3f}")
```

**Refresh the MLflow UI** - you'll see 3 runs, sortable by accuracy.

**Test 2: Compare runs**

In the MLflow UI:
1. Check the boxes next to multiple runs
2. Click "Compare"
3. See parameters and metrics side-by-side

✅ **If you can see and compare runs, your MLflow installation is working perfectly!**

---

## Level 3: Core Concepts

MLflow's power comes from understanding 5 fundamental concepts. Master these, and you'll understand 80% of MLflow.

### Concept 1: Runs

**What is a Run?**

A **run** is a single execution of your ML code. Every time you train a model, that's one run.

Each run captures:
- **Parameters**: Inputs to your model (learning_rate, n_estimators, batch_size)
- **Metrics**: Outputs/results (accuracy, loss, F1 score)
- **Artifacts**: Files produced (trained model, plots, datasets)
- **Metadata**: When it ran, how long it took, who ran it, what code version

**Example: Creating a Run**

```python
import mlflow
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Load data
X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Start a run
with mlflow.start_run():
    # Define and train model
    n_estimators = 100
    max_depth = 5

    model = RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        random_state=42
    )
    model.fit(X_train, y_train)

    # Evaluate
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)

    # Log everything to MLflow
    mlflow.log_param("n_estimators", n_estimators)
    mlflow.log_param("max_depth", max_depth)
    mlflow.log_metric("accuracy", accuracy)

    print(f"✅ Run complete. Accuracy: {accuracy:.3f}")
```

**Why it matters**: Runs give you complete reproducibility. Six months later, you can look at a run and know exactly what produced that model.

**Common Mistake**:
❌ Forgetting to call `mlflow.start_run()` - logging functions will fail
✅ Always wrap your training code in `with mlflow.start_run():`

---

### Concept 2: Experiments

**What is an Experiment?**

An **experiment** is a collection of related runs. Think of it as a folder that groups runs working toward the same goal.

**Example use cases**:
- Experiment: "customer_churn_prediction" → Contains 50 runs with different models
- Experiment: "hyperparameter_tuning_xgboost" → Contains 100 runs with different hyperparameters
- Experiment: "weekly_model_retrain" → Contains runs from each week's training job

**Example: Creating Experiments**

```python
import mlflow

# Create or set an experiment
mlflow.set_experiment("iris_classification_v2")

# Now all runs go into this experiment
for max_depth in [3, 5, 10, 20]:
    with mlflow.start_run():
        mlflow.log_param("max_depth", max_depth)
        # ... train and log metrics ...
```

**Organizing Multiple Experiments**

```python
import mlflow

# Experiment 1: Random Forest tuning
mlflow.set_experiment("iris_random_forest")
with mlflow.start_run(run_name="rf_baseline"):
    mlflow.log_param("model_type", "random_forest")
    # ... training code ...

# Experiment 2: XGBoost tuning
mlflow.set_experiment("iris_xgboost")
with mlflow.start_run(run_name="xgb_baseline"):
    mlflow.log_param("model_type", "xgboost")
    # ... training code ...
```

**Why it matters**: Experiments keep your tracking organized. Without them, all runs pile up in one "Default" experiment, making it impossible to find anything.

**Common Mistake**:
❌ Putting unrelated runs in the same experiment
✅ Create separate experiments for different models, datasets, or goals

---

### Concept 3: Model Registry

**What is the Model Registry?**

The **Model Registry** is a centralized hub for managing model lifecycles. It's like GitHub for ML models - versioning, staging, and deployment management.

**Model Lifecycle Stages**:
1. **None**: Just registered, not yet assigned a stage
2. **Staging**: Ready for testing in a staging environment
3. **Production**: Deployed to production
4. **Archived**: Retired models

**Example: Registering a Model**

```python
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris

# Train a model
X, y = load_iris(return_X_y=True)
model = RandomForestClassifier(n_estimators=100)
model.fit(X, y)

# Log and register the model
with mlflow.start_run():
    mlflow.sklearn.log_model(
        sk_model=model,
        artifact_path="model",
        registered_model_name="iris_classifier"  # This registers it!
    )
    mlflow.log_param("n_estimators", 100)
```

**Working with Registered Models**

```python
from mlflow.tracking import MlflowClient

client = MlflowClient()

# List all registered models
for model in client.search_registered_models():
    print(f"Model: {model.name}")

# Get latest version
model_name = "iris_classifier"
latest_version = client.get_latest_versions(model_name, stages=["None"])[0]
print(f"Latest version: {latest_version.version}")

# Transition to Production
client.transition_model_version_stage(
    name=model_name,
    version=latest_version.version,
    stage="Production"
)
```

**Loading a Production Model**

```python
import mlflow.pyfunc

# Load the production model
model_uri = "models:/iris_classifier/Production"
model = mlflow.pyfunc.load_model(model_uri)

# Use it for predictions
predictions = model.predict(new_data)
```

**Why it matters**: The registry creates a single source of truth for models. Teams know which model is in production, can roll back if needed, and have full version history.

**Common Mistake**:
❌ Registering every training run as a new model version (creates clutter)
✅ Only register models that pass quality thresholds

---

### Concept 4: Autologging

**What is Autologging?**

**Autologging** automatically captures parameters, metrics, and models WITHOUT manual logging code. It's MLflow's "magic mode."

**One line of code tracks everything**:

```python
import mlflow

mlflow.autolog()  # That's it!

# Now train normally - MLflow logs everything automatically
from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier(n_estimators=100, max_depth=5)
model.fit(X_train, y_train)
# MLflow automatically logged: n_estimators, max_depth, accuracy, model artifact
```

**What Gets Logged Automatically?**

**For scikit-learn**:
- All model hyperparameters
- Training metrics (accuracy, precision, recall, F1)
- The trained model
- Feature importance plots

**For PyTorch**:
- Model hyperparameters
- Training and validation loss
- Model checkpoints
- Learning rate schedules

**For TensorFlow/Keras**:
- Model architecture
- Training history (loss, accuracy per epoch)
- Model weights
- TensorBoard logs

**Example: Autologging with Multiple Frameworks**

```python
import mlflow

# Enable autologging globally
mlflow.autolog()

# Scikit-learn example
from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)
# ✅ Automatically logged: params, metrics, model

# XGBoost example
import xgboost as xgb
dtrain = xgb.DMatrix(X_train, label=y_train)
params = {"max_depth": 5, "eta": 0.1}
bst = xgb.train(params, dtrain, num_boost_round=100)
# ✅ Automatically logged: params, metrics, model
```

**Framework-Specific Autologging**

```python
# Enable autologging for specific framework only
import mlflow.sklearn
mlflow.sklearn.autolog()

# Or for PyTorch
import mlflow.pytorch
mlflow.pytorch.autolog()

# Or for TensorFlow
import mlflow.tensorflow
mlflow.tensorflow.autolog()
```

**Why it matters**: Autologging eliminates 90% of boilerplate logging code. You focus on model building, MLflow handles tracking.

**Common Mistake**:
❌ Calling `mlflow.autolog()` inside the `start_run()` block (too late!)
✅ Call `mlflow.autolog()` BEFORE creating/training your model

**When to use manual logging instead**:
- Custom metrics not captured automatically
- Domain-specific metadata
- Fine-grained control over what gets logged
- Logging non-standard artifacts (reports, custom plots)

---

### Concept 5: Model Flavors

**What are Model Flavors?**

A **flavor** is MLflow's way of packaging models from different frameworks in a standard format. Think of it as a universal adapter.

**Every MLflow model has TWO flavors**:
1. **Framework-specific flavor** (sklearn, pytorch, tensorflow, xgboost, etc.)
2. **pyfunc flavor** (Python function - generic interface)

**Why Flavors Matter**:

Without flavors:
- Scikit-learn models loaded with `joblib`
- PyTorch models loaded with `torch.load()`
- TensorFlow models loaded with `tf.keras.models.load_model()`
- Every framework is different!

With MLflow flavors:
- ALL models loaded with `mlflow.pyfunc.load_model()`
- Unified `model.predict()` interface
- Deploy any model the same way

**Example: Model Flavors in Action**

```python
import mlflow
import mlflow.sklearn
import mlflow.pytorch
from sklearn.ensemble import RandomForestClassifier
import torch.nn as nn

# Log a scikit-learn model
with mlflow.start_run():
    sklearn_model = RandomForestClassifier()
    sklearn_model.fit(X_train, y_train)

    mlflow.sklearn.log_model(
        sk_model=sklearn_model,
        artifact_path="sklearn_model"
    )

# Log a PyTorch model
with mlflow.start_run():
    pytorch_model = nn.Sequential(nn.Linear(10, 5), nn.ReLU())

    mlflow.pytorch.log_model(
        pytorch_model=pytorch_model,
        artifact_path="pytorch_model"
    )

# Load both using the SAME interface
sklearn_loaded = mlflow.pyfunc.load_model("runs:/<run_id>/sklearn_model")
pytorch_loaded = mlflow.pyfunc.load_model("runs:/<run_id>/pytorch_model")

# Predict using the SAME interface
sklearn_predictions = sklearn_loaded.predict(X_test)
pytorch_predictions = pytorch_loaded.predict(X_test)
```

**Available Flavors**:
- `mlflow.sklearn` - Scikit-learn
- `mlflow.pytorch` - PyTorch
- `mlflow.tensorflow` - TensorFlow
- `mlflow.keras` - Keras
- `mlflow.xgboost` - XGBoost
- `mlflow.lightgbm` - LightGBM
- `mlflow.catboost` - CatBoost
- `mlflow.spark` - PySpark ML
- `mlflow.h2o` - H2O
- `mlflow.onnx` - ONNX
- `mlflow.langchain` - LangChain
- `mlflow.openai` - OpenAI
- `mlflow.transformers` - Hugging Face Transformers
- `mlflow.pyfunc` - Custom Python functions

**Creating Custom Flavors**

```python
import mlflow.pyfunc

# Define a custom model
class CustomModel(mlflow.pyfunc.PythonModel):
    def load_context(self, context):
        # Load any dependencies
        pass

    def predict(self, context, model_input):
        # Your custom prediction logic
        return model_input * 2

# Log the custom model
with mlflow.start_run():
    mlflow.pyfunc.log_model(
        artifact_path="custom_model",
        python_model=CustomModel()
    )
```

**Why it matters**: Flavors enable framework-agnostic deployment. You can switch from scikit-learn to XGBoost without changing deployment code.

**Common Mistake**:
❌ Using `pickle.dump()` or `joblib.dump()` to save models manually
✅ Always use `mlflow.<flavor>.log_model()` for proper tracking and packaging

---

### How Concepts Relate

```
EXPERIMENT (e.g., "customer_churn_prediction")
  └── RUN 1 (Random Forest, n_estimators=100)
       ├── Parameters: {n_estimators: 100, max_depth: 5}
       ├── Metrics: {accuracy: 0.92, f1_score: 0.89}
       └── Artifacts: model (sklearn flavor + pyfunc flavor)
  └── RUN 2 (XGBoost, max_depth=10)
       ├── Parameters: {max_depth: 10, learning_rate: 0.1}
       ├── Metrics: {accuracy: 0.94, f1_score: 0.91}
       └── Artifacts: model (xgboost flavor + pyfunc flavor)
  └── RUN 3 (Neural Network)
       └── ...

MODEL REGISTRY
  └── "churn_classifier" (registered model name)
       ├── Version 1 (from RUN 1) - Stage: Archived
       ├── Version 2 (from RUN 2) - Stage: Production ← Best model
       └── Version 3 (from RUN 3) - Stage: Staging

AUTOLOGGING: Automatically creates Parameters, Metrics, Artifacts
FLAVORS: Standardize how models are saved and loaded
```

**Summary**: Master these 5 concepts, and you understand the MLflow mental model. Everything else builds on this foundation.

---

## Level 4: Practical Patterns

Now let's apply the core concepts to real-world scenarios, progressively building from simple to complex.

### Pattern 1: Basic Training Script with Tracking

**Scenario**: You're training a classification model and want to track experiments.

**Code**: `code-examples/02-core-concepts/basic_training.py`

```python
import mlflow
import mlflow.sklearn
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, precision_score

# Set experiment name
mlflow.set_experiment("wine_classification")

# Load data
X, y = load_wine(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Enable autologging
mlflow.sklearn.autolog()

# Train model
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

    # Log additional custom metrics
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
    print(f"   Accuracy: {accuracy:.3f}")
    print(f"   F1 Score: {f1:.3f}")
```

**What this demonstrates**:
- Setting up an experiment
- Using autologging for automatic parameter tracking
- Logging custom metrics beyond what autologging captures
- Registering the model for future deployment

**Run it**: `python basic_training.py`

---

### Pattern 2: Hyperparameter Tuning with MLflow

**Scenario**: You want to find the best hyperparameters for your model and track all attempts.

**Code**: `code-examples/03-patterns/hyperparameter_tuning.py`

```python
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
X, y = load_wine(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Define hyperparameter grid
n_estimators_options = [50, 100, 200]
max_depth_options = [5, 10, 20]
min_samples_split_options = [2, 5, 10]

# Create a parent run for the tuning session
with mlflow.start_run(run_name="hyperparameter_tuning_session") as parent_run:

    # Try all combinations
    best_accuracy = 0
    best_params = {}

    for n_est, max_d, min_split in product(
        n_estimators_options, max_depth_options, min_samples_split_options
    ):
        # Create a child run for each hyperparameter combination
        with mlflow.start_run(run_name=f"n{n_est}_d{max_d}_s{min_split}", nested=True):
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
                mlflow.sklearn.log_model(model, "model")

            print(f"n_est={n_est}, max_d={max_d}, min_split={min_split} → accuracy={accuracy:.3f}")

    # Log best results to parent run
    mlflow.log_params(best_params)
    mlflow.log_metric("best_accuracy", best_accuracy)

    print(f"\n🏆 Best accuracy: {best_accuracy:.3f}")
    print(f"🏆 Best params: {best_params}")
```

**What this demonstrates**:
- Nested runs (parent for tuning session, children for each combination)
- Systematic hyperparameter exploration
- Tracking the best model across all runs
- Organizing related runs hierarchically

**Advanced: Using Optuna with MLflow**

```python
import mlflow
import optuna
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

def objective(trial):
    # Suggest hyperparameters
    n_estimators = trial.suggest_int("n_estimators", 10, 200)
    max_depth = trial.suggest_int("max_depth", 2, 32)

    # Train model
    model = RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        random_state=42
    )
    model.fit(X_train, y_train)

    # Evaluate
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)

    # Log to MLflow
    mlflow.log_params(trial.params)
    mlflow.log_metric("accuracy", accuracy)

    return accuracy

# Run optimization
mlflow.set_experiment("optuna_tuning")
with mlflow.start_run():
    study = optuna.create_study(direction="maximize")
    study.optimize(objective, n_trials=50)

    print(f"Best accuracy: {study.best_value:.3f}")
    print(f"Best params: {study.best_params}")
```

---

### Pattern 3: Production Model Deployment

**Scenario**: You've trained a model, registered it, and now want to deploy it for inference.

**Step 1: Train and Register**

```python
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier

mlflow.set_experiment("production_deployment")

with mlflow.start_run():
    # Train model
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X_train, y_train)

    # Register model
    mlflow.sklearn.log_model(
        sk_model=model,
        artifact_path="model",
        registered_model_name="production_wine_classifier"
    )
```

**Step 2: Promote to Production**

```python
from mlflow.tracking import MlflowClient

client = MlflowClient()

# Get the latest model version
model_name = "production_wine_classifier"
latest_version = client.get_latest_versions(model_name, stages=["None"])[0]

# Transition to Production
client.transition_model_version_stage(
    name=model_name,
    version=latest_version.version,
    stage="Production",
    archive_existing_versions=True  # Archive previous production version
)

print(f"✅ Model version {latest_version.version} is now in Production")
```

**Step 3: Load and Serve**

```python
import mlflow.pyfunc
import pandas as pd

# Load the production model
model_uri = "models:/production_wine_classifier/Production"
model = mlflow.pyfunc.load_model(model_uri)

# Create a prediction function
def predict(input_data):
    """
    Prediction function for serving.

    Args:
        input_data: pandas DataFrame with feature columns

    Returns:
        predictions: numpy array of predictions
    """
    predictions = model.predict(input_data)
    return predictions

# Example usage
new_data = pd.DataFrame({
    'alcohol': [13.2],
    'malic_acid': [2.5],
    # ... other features ...
})

predictions = predict(new_data)
print(f"Prediction: {predictions}")
```

**Step 4: Deploy as REST API**

MLflow can serve models as REST APIs with one command:

```bash
# Serve the production model on port 5001
mlflow models serve \
    --model-uri "models:/production_wine_classifier/Production" \
    --port 5001 \
    --no-conda
```

**Step 5: Make Predictions via HTTP**

```python
import requests
import json

url = "http://127.0.0.1:5001/invocations"
headers = {"Content-Type": "application/json"}

# Prepare input data
data = {
    "inputs": [[13.2, 2.5, 2.6, 20.0, 100, 2.8, 3.1, 0.3, 2.1, 5.5, 1.0, 3.2, 1100]]
}

# Make prediction
response = requests.post(url, headers=headers, data=json.dumps(data))
predictions = response.json()

print(f"Prediction: {predictions}")
```

**What this demonstrates**:
- Complete model lifecycle (train → register → promote → deploy)
- Model versioning and stage management
- Serving models as REST APIs
- Production-ready prediction pipelines

---

### Pattern 4: LLM Application Tracing

**Scenario**: You're building an LLM application and want to trace interactions for debugging and evaluation.

**Code**: `code-examples/03-patterns/llm_tracing.py`

```python
import mlflow
from openai import OpenAI

# Enable autologging for OpenAI
mlflow.openai.autolog()

client = OpenAI()

# Set experiment
mlflow.set_experiment("customer_support_chatbot")

# Trace a conversation
with mlflow.start_run(run_name="support_conversation_001"):

    # User query
    user_message = "How do I reset my password?"

    # LLM call (automatically traced)
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful customer support agent."},
            {"role": "user", "content": user_message}
        ],
        temperature=0.7,
        max_tokens=150
    )

    assistant_message = response.choices[0].message.content

    # Log additional context
    mlflow.log_param("user_query", user_message)
    mlflow.log_metric("response_tokens", response.usage.completion_tokens)
    mlflow.log_metric("total_tokens", response.usage.total_tokens)

    print(f"User: {user_message}")
    print(f"Assistant: {assistant_message}")

# View traces in MLflow UI under "Traces" tab
```

**Advanced: Multi-Step LLM Pipeline**

```python
import mlflow
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

# Enable LangChain autologging
mlflow.langchain.autolog()

mlflow.set_experiment("rag_pipeline")

with mlflow.start_run(run_name="rag_query"):

    # Define prompt template
    template = """
    Context: {context}

    Question: {question}

    Answer the question based on the context above.
    """

    prompt = PromptTemplate(template=template, input_variables=["context", "question"])

    # Create chain
    llm = ChatOpenAI(model="gpt-4", temperature=0.3)
    chain = LLMChain(llm=llm, prompt=prompt)

    # Run chain (automatically traced)
    result = chain.run(
        context="MLflow is an open-source platform for ML lifecycle management.",
        question="What is MLflow?"
    )

    print(f"Answer: {result}")

# MLflow automatically captures:
# - Prompt templates
# - LLM calls
# - Chain execution flow
# - Token usage
# - Latency
```

**What this demonstrates**:
- Automatic LLM tracing without manual instrumentation
- Token usage tracking for cost monitoring
- Multi-step pipeline observability
- Integration with LangChain and OpenAI

---

### Pattern 5: Model Evaluation and Comparison

**Scenario**: You've trained multiple models and want to systematically compare them.

**Code**: `code-examples/03-patterns/model_comparison.py`

```python
import mlflow
from mlflow.tracking import MlflowClient
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

mlflow.set_experiment("model_comparison")

# Define models to compare
models = {
    "random_forest": RandomForestClassifier(n_estimators=100, random_state=42),
    "gradient_boosting": GradientBoostingClassifier(n_estimators=100, random_state=42),
    "logistic_regression": LogisticRegression(max_iter=1000, random_state=42)
}

results = []

# Train and evaluate each model
for model_name, model in models.items():
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

        # Save results
        results.append({
            "model": model_name,
            **metrics
        })

        print(f"{model_name}: accuracy={metrics['accuracy']:.3f}")

# Create comparison DataFrame
comparison_df = pd.DataFrame(results)
print("\n📊 Model Comparison:")
print(comparison_df.sort_values("accuracy", ascending=False))

# Query best model programmatically
client = MlflowClient()
experiment = client.get_experiment_by_name("model_comparison")
runs = client.search_runs(
    experiment_ids=[experiment.experiment_id],
    order_by=["metrics.accuracy DESC"],
    max_results=1
)

best_run = runs[0]
print(f"\n🏆 Best Model: {best_run.data.params['model_type']}")
print(f"   Accuracy: {best_run.data.metrics['accuracy']:.3f}")
```

**Using MLflow's Built-in Evaluation**

```python
import mlflow

# Evaluate a logged model
eval_data = pd.DataFrame({
    "features": X_test.tolist(),
    "labels": y_test.tolist()
})

result = mlflow.evaluate(
    model="runs:/<run_id>/model",
    data=eval_data,
    targets="labels",
    model_type="classifier",
    evaluators=["default"]
)

print(result.metrics)  # Automatic metrics computation
print(result.artifacts)  # Generated plots and reports
```

---

### Pattern 6: Team Collaboration with Remote Tracking

**Scenario**: Your team wants to share experiment results using a central MLflow server.

**Setup: Remote Tracking Server**

```bash
# Start MLflow server with PostgreSQL backend and S3 artifacts
mlflow server \
    --backend-store-uri postgresql://user:password@localhost/mlflow_db \
    --default-artifact-root s3://my-mlflow-bucket/artifacts \
    --host 0.0.0.0 \
    --port 5000
```

**Client Code: Point to Remote Server**

```python
import mlflow
import os

# Configure remote tracking
os.environ["MLFLOW_TRACKING_URI"] = "http://mlflow-server.company.com:5000"

# Or set programmatically
mlflow.set_tracking_uri("http://mlflow-server.company.com:5000")

# Now all logging goes to the remote server
mlflow.set_experiment("team_shared_experiment")

with mlflow.start_run():
    mlflow.log_param("team_member", "alice")
    # ... train and log ...
```

**What this demonstrates**:
- Centralized tracking for team collaboration
- Persistent storage with PostgreSQL
- Cloud artifact storage (S3, GCS, Azure Blob)
- Shared experiment visibility across the team

---

## Level 5: Next Steps

Congratulations! You've mastered the fundamentals of MLflow. Here's how to continue your journey.

### Advanced Topics to Explore

#### 1. MLflow Projects
**What**: Packaging ML code in a reproducible format with dependencies.

**Learn more**:
- [MLflow Projects Documentation](https://mlflow.org/docs/latest/projects.html)
- Use cases: Reproducible training, CI/CD integration
- Example: Docker-based projects

**Quick example**:
```yaml
# MLproject file
name: my_project
conda_env: conda.yaml

entry_points:
  main:
    parameters:
      learning_rate: {type: float, default: 0.01}
    command: "python train.py --lr {learning_rate}"
```

Run with: `mlflow run . -P learning_rate=0.001`

---

#### 2. Model Deployment Strategies

**Deployment Options**:
- **MLflow Models CLI**: `mlflow models serve`
- **Docker**: Containerized deployment
- **Kubernetes**: Scalable serving with KServe
- **Cloud Platforms**: AWS SageMaker, Azure ML, GCP Vertex AI
- **Batch Inference**: Spark UDF for large-scale predictions

**Learn more**:
- [MLflow Deployment Guide](https://mlflow.org/docs/latest/deployment/index.html)
- [Docker Deployment](https://mlflow.org/docs/latest/deployment/deploy-model-locally.html)

**Example: Docker deployment**:
```bash
# Build Docker image for your model
mlflow models build-docker \
    --model-uri "models:/my_model/Production" \
    --name "my-model-image"

# Run container
docker run -p 5001:8080 my-model-image
```

---

#### 3. LLM Evaluation and Prompt Engineering

**What**: Systematically evaluate LLM outputs for quality, correctness, and safety.

**Learn more**:
- [MLflow LLM Evaluation](https://mlflow.org/docs/latest/llms/llm-evaluate/index.html)
- Built-in metrics: Correctness, Guidelines, Relevance
- Custom evaluators for domain-specific criteria

**Example**:
```python
import mlflow

# Evaluate LLM responses
eval_data = pd.DataFrame({
    "inputs": ["What is MLflow?", "How do I install it?"],
    "ground_truth": ["MLflow is an ML platform", "pip install mlflow"]
})

with mlflow.start_run():
    results = mlflow.evaluate(
        data=eval_data,
        model_type="question-answering",
        evaluators=["default"]
    )
```

---

#### 4. Custom Plugins and Extensions

**What**: Extend MLflow with custom tracking backends, artifact stores, or model flavors.

**Learn more**:
- [MLflow Plugins](https://mlflow.org/docs/latest/plugins.html)
- Create custom tracking stores
- Build custom model flavors

---

#### 5. MLflow at Scale

**Topics**:
- Distributed training with Spark
- Managing thousands of experiments
- Performance optimization
- Database tuning for large deployments

**Learn more**:
- [MLflow on Databricks](https://docs.databricks.com/mlflow/index.html)
- [Spark MLflow Integration](https://mlflow.org/docs/latest/python_api/mlflow.spark.html)

---

### Best Resources for Each Topic

#### Official Documentation
1. **MLflow Docs**: https://mlflow.org/docs/latest/
   - Comprehensive, well-maintained, always up-to-date

2. **MLflow GitHub**: https://github.com/mlflow/mlflow
   - Source code, examples, issue tracking

3. **MLflow Blog**: https://mlflow.org/blog
   - New features, case studies, best practices

#### Online Courses

1. **"Introduction to MLflow"** - LinkedIn Learning (Databricks)
   - 🎥 Video course
   - Official Databricks content
   - Production best practices

2. **"Practical Deep Learning at Scale with MLflow"** by Yong Liu
   - 📖 Book
   - Deep learning focus
   - Advanced deployment patterns

3. **"MLOps Specialization"** - Coursera (DeepLearning.AI)
   - Includes MLflow in broader MLOps context
   - Andrew Ng's teaching style

#### Tutorials & Blogs

1. **Ander Fernández Jauregui's MLflow Tutorial**
   - https://anderfernandez.com/en/blog/complete-mlflow-tutorial/
   - Production setup with cloud storage
   - PostgreSQL backend configuration

2. **Towards Data Science MLflow Articles**
   - Search: "MLflow" on TDS
   - Community tutorials and case studies

3. **Real Python MLflow Guide**
   - Beginner-friendly
   - Step-by-step examples

#### Community Resources

**Slack**: https://go.mlflow.org/slack
- Active community
- Quick answers to questions
- Share tips and tricks

**GitHub Discussions**: https://github.com/mlflow/mlflow/discussions
- Technical deep-dives
- Feature discussions
- Troubleshooting

**Stack Overflow**: Tag `mlflow`
- 2,000+ answered questions
- Common issues and solutions

**YouTube Channels**:
- Databricks official channel
- MLOps community creators
- Conference talks (apply.co, MLOps World)

---

### How to Get Help

#### When You're Stuck

1. **Check the docs first**: https://mlflow.org/docs/latest/
2. **Search GitHub issues**: Likely someone had the same problem
3. **Ask on Slack**: Real-time community support
4. **Post on Stack Overflow**: Detailed Q&A with examples
5. **Read the source code**: MLflow is open-source - the code is the truth

#### Debugging Tips

**Enable debug logging**:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

**Check MLflow tracking directory**:
```bash
ls -la mlruns/
cat mlruns/0/<run_id>/meta.yaml
```

**Inspect logged artifacts**:
```python
from mlflow.tracking import MlflowClient

client = MlflowClient()
artifacts = client.list_artifacts(run_id)
for artifact in artifacts:
    print(artifact.path)
```

---

### Mini-Project: Build a Complete ML Pipeline

**Objective**: Apply everything you've learned by building an end-to-end ML pipeline with MLflow.

**Project: Customer Churn Prediction System**

**Requirements**:
1. ✅ Track experiments with multiple algorithms (Logistic Regression, Random Forest, XGBoost)
2. ✅ Perform hyperparameter tuning and log all runs
3. ✅ Register the best model to the Model Registry
4. ✅ Transition the model to Production
5. ✅ Deploy the model as a REST API
6. ✅ Create a prediction script that uses the production model
7. ✅ Document your experiments in the MLflow UI

**Bonus Challenges**:
- 🚀 Set up a remote tracking server with PostgreSQL
- 🚀 Store artifacts in S3/GCS/Azure Blob
- 🚀 Create a CI/CD pipeline that automatically deploys models above accuracy threshold
- 🚀 Build a Streamlit dashboard that queries the MLflow API to show model performance over time

**Starter Code Structure**:
```
churn-prediction/
├── data/
│   └── churn_data.csv
├── notebooks/
│   └── exploration.ipynb
├── src/
│   ├── train.py              # Training script with MLflow tracking
│   ├── tune_hyperparams.py   # Hyperparameter tuning
│   ├── register_model.py     # Model registration
│   └── predict.py            # Prediction using production model
├── deploy/
│   └── serve_model.sh        # Deployment script
├── MLproject                 # MLflow project definition
├── conda.yaml                # Environment specification
└── README.md
```

**Timeline**: 4-6 hours for complete implementation

---

### Your MLflow Learning Roadmap

**Week 1: Foundations**
- ✅ Complete Levels 1-3 of this learning path
- ✅ Run all code examples
- ✅ Set up MLflow UI and explore interface

**Week 2: Practice**
- ✅ Complete Level 4 patterns
- ✅ Track a real ML project with MLflow
- ✅ Experiment with different frameworks (scikit-learn, XGBoost, PyTorch)

**Week 3: Production**
- ✅ Set up remote tracking server
- ✅ Deploy a model as REST API
- ✅ Integrate MLflow into existing workflows

**Week 4: Advanced**
- ✅ Explore MLflow Projects
- ✅ Build custom model flavors
- ✅ Complete the mini-project

**Ongoing**:
- 📚 Follow MLflow blog for new features
- 👥 Engage with community on Slack
- 🔧 Contribute to MLflow (report issues, improve docs, submit PRs)

---

### Final Tips for Success

1. **Start small, iterate**: Begin with basic tracking, add complexity gradually
2. **Use autologging**: Let MLflow handle the boilerplate, focus on modeling
3. **Organize experiments**: Name experiments clearly, use tags consistently
4. **Leverage the UI**: Visual comparison is powerful for understanding model performance
5. **Document decisions**: Use MLflow tags and notes to record why you made choices
6. **Share with team**: Central tracking server enables collaboration
7. **Automate deployment**: Use Model Registry stages to trigger automated deployments
8. **Monitor production models**: Track inference metrics alongside training metrics

---

**You've completed the MLflow learning path!** 🎉

You now have:
- ✅ Solid understanding of MLflow's purpose and architecture
- ✅ Hands-on experience with core concepts (Runs, Experiments, Registry, Autologging, Flavors)
- ✅ Practical patterns for real-world scenarios
- ✅ Resources to continue learning
- ✅ A mini-project to solidify your knowledge

**Next steps**: Pick a real ML project and integrate MLflow today. The best way to learn is by doing.

**Good luck, and happy MLflow-ing!** 🚀
