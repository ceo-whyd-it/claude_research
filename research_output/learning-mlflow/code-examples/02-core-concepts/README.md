# Core Concepts Examples

Examples demonstrating MLflow's five fundamental concepts.

## Files

### `basic_training.py`
Complete training workflow showing runs, experiments, and model logging.

**Run it**:
```bash
python basic_training.py
```

**Demonstrates**:
- Creating an experiment
- Using autologging
- Logging custom metrics
- Registering a model

### `experiments_demo.py`
Shows how to organize runs into experiments.

**Run it**:
```bash
python experiments_demo.py
```

**Demonstrates**:
- Creating multiple experiments
- Organizing related runs
- Naming runs for clarity

### `autologging_demo.py`
The power of autologging with scikit-learn and XGBoost.

**Run it**:
```bash
pip install xgboost  # If not already installed
python autologging_demo.py
```

**Demonstrates**:
- Global autologging with `mlflow.autolog()`
- Framework-specific autologging
- What gets logged automatically
- Combining autologging with manual logging

### `model_registry_demo.py`
Complete model lifecycle management.

**Run it**:
```bash
python model_registry_demo.py
```

**Demonstrates**:
- Registering models
- Model versioning
- Stage transitions (None → Staging → Production)
- Loading models by stage
- Listing registered models

## Prerequisites

```bash
pip install mlflow scikit-learn xgboost
```

## Key Takeaways

After running these examples, you'll understand:

1. **Runs**: Individual executions of ML code
2. **Experiments**: Collections of related runs
3. **Model Registry**: Centralized model version control
4. **Autologging**: Automatic parameter/metric tracking
5. **Model Flavors**: Framework-agnostic model packaging

## Next Steps

After mastering these concepts, move on to `03-patterns/` for real-world use cases.
