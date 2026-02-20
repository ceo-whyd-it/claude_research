# Practical Patterns

Real-world MLflow patterns for production use cases.

## Files

### `hyperparameter_tuning.py`
Systematic hyperparameter search with nested runs.

**Run it**:
```bash
python hyperparameter_tuning.py
```

**Demonstrates**:
- Grid search over hyperparameter space
- Nested runs (parent for session, children for each combination)
- Tracking best parameters across all runs
- Hierarchical organization of experiments

**Output**: Tests 27 hyperparameter combinations and identifies the best.

---

### `model_comparison.py`
Compare multiple ML algorithms side-by-side.

**Run it**:
```bash
python model_comparison.py
```

**Demonstrates**:
- Training multiple model types (Random Forest, Gradient Boosting, Logistic Regression, SVM)
- Logging standardized metrics across all models
- Querying the best model programmatically via MLflow API
- Creating comparison tables

**Output**: Comparison table showing accuracy, F1, precision, and recall for each model.

---

### `production_deployment.py`
Complete production deployment workflow.

**Run it**:
```bash
python production_deployment.py
```

**Demonstrates**:
- Training and registering a model
- Promoting to Production stage
- Loading production models
- Making predictions
- Deployment options (REST API, Docker, Cloud)

**Output**: Step-by-step deployment guide with commands.

---

## Prerequisites

```bash
pip install mlflow scikit-learn pandas numpy
```

## Usage Patterns

### Pattern 1: Hyperparameter Tuning

Best for:
- Finding optimal model configuration
- Systematic parameter exploration
- Comparing many variations

When to use:
- Before final model selection
- When model performance is critical
- When you have computational budget for search

### Pattern 2: Model Comparison

Best for:
- Choosing between algorithms
- Benchmarking approaches
- A/B testing different models

When to use:
- At project start (baseline comparison)
- When exploring new algorithms
- For regular model refresh cycles

### Pattern 3: Production Deployment

Best for:
- Moving models to production
- Version control in production
- Safe rollback capability

When to use:
- After model validation
- For production serving
- When you need deployment automation

## Real-World Tips

**Hyperparameter Tuning**:
- Start with coarse grid, then refine
- Use Optuna for Bayesian optimization
- Track computational cost (time, resources)

**Model Comparison**:
- Use consistent evaluation metrics
- Test on same train/test split
- Consider inference speed, not just accuracy

**Production Deployment**:
- Always test in staging before production
- Use model aliases for zero-downtime swaps
- Monitor production model performance

## Next Steps

1. Run all three patterns on your own dataset
2. Combine patterns (e.g., tune → compare → deploy)
3. Integrate with your CI/CD pipeline
4. Explore cloud deployment options

## Advanced Patterns (Not Included)

For further exploration:
- **A/B Testing**: Deploy multiple models, compare in production
- **Model Monitoring**: Track drift and degradation
- **Automated Retraining**: Trigger based on performance thresholds
- **Multi-Model Serving**: Serve ensemble or multiple models
