# Hello World Examples

Simple examples to verify your MLflow installation is working.

## Files

### `hello_mlflow.py`
The absolute simplest MLflow example - logs one parameter and one metric.

**Run it**:
```bash
python hello_mlflow.py
```

**What it does**:
- Creates a run with `mlflow.start_run()`
- Logs a parameter: `learning_rate=0.01`
- Logs a metric: `accuracy=0.95`
- Stores everything in `mlruns/` directory

### `multiple_runs.py`
Runs three experiments with different learning rates.

**Run it**:
```bash
python multiple_runs.py
```

**What it does**:
- Creates 3 separate runs
- Each run has a different `learning_rate` parameter
- Shows how to compare multiple experiments

## Viewing Results

After running either script:

1. Start the MLflow UI:
   ```bash
   mlflow ui
   ```

2. Open your browser to `http://127.0.0.1:5000`

3. Explore:
   - Click on runs to see details
   - Compare runs side-by-side
   - Sort by metrics
   - View parameters and metadata

## Expected Output

```
✅ Logged: learning_rate=0.01, accuracy=0.95

🎉 Success! Your first MLflow experiment is logged.
👉 Run 'mlflow ui' to view results in the web interface
```

## Troubleshooting

**Issue**: `ModuleNotFoundError: No module named 'mlflow'`
**Solution**: Install MLflow with `pip install mlflow`

**Issue**: `mlruns/` directory not created
**Solution**: Check you have write permissions in the current directory

**Issue**: MLflow UI shows no experiments
**Solution**: Make sure you're running `mlflow ui` from the same directory where you ran the Python scripts
