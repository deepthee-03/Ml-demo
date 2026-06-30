# =============================================================================
# predict.py — Load the saved model and predict the Iris flower species
# =============================================================================
# This script:
#   1. Loads iris_model.pkl from disk
#   2. Accepts a sample input (sepal length, sepal width, petal length,
#      petal width) in centimetres
#   3. Predicts and prints the flower species name
# =============================================================================

import joblib
import numpy as np
from sklearn.datasets import load_iris

# ── 1. Load the saved model ───────────────────────────────────────────────────
model_path = "iris_model.pkl"
model = joblib.load(model_path)
print(f"Model loaded from: {model_path}")

# ── 2. Load target-name mapping (setosa / versicolor / virginica) ─────────────
iris = load_iris()
target_names = iris.target_names   # ['setosa', 'versicolor', 'virginica']

# ── 3. Define sample inputs ───────────────────────────────────────────────────
# Each row: [sepal_length_cm, sepal_width_cm, petal_length_cm, petal_width_cm]
sample_inputs = [
    [5.1, 3.5, 1.4, 0.2],   # Expected: setosa
    [6.7, 3.0, 5.2, 2.3],   # Expected: virginica
    [5.9, 3.0, 4.2, 1.5],   # Expected: versicolor
]

# ── 4. Predict and display results ────────────────────────────────────────────
print("\n" + "=" * 60)
print("          IRIS FLOWER SPECIES PREDICTIONS")
print("=" * 60)
print(f"  {'#':<4} {'Input (cm)':<36} {'Predicted Species'}")
print("  " + "-" * 56)

for idx, sample in enumerate(sample_inputs, start=1):
    # model.predict expects a 2-D array — reshape the 1-D list accordingly
    input_array = np.array(sample).reshape(1, -1)
    prediction_index = model.predict(input_array)[0]
    predicted_species = target_names[prediction_index]

    input_str = str(sample)
    print(f"  {idx:<4} {input_str:<36} {predicted_species.capitalize()}")

print("=" * 60)
