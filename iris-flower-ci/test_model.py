# =============================================================================
# test_model.py — pytest unit tests for the Iris Classification project
# =============================================================================
# Tests covered:
#   1. Model file exists after training
#   2. Loaded model can make predictions on a valid input
#   3. Model accuracy on the full Iris test split is >= 90 %
# =============================================================================

import os

import joblib
import numpy as np
import pytest
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

# Path where the trained model is expected to be saved
MODEL_PATH = "iris_model.pkl"


# ─── Fixtures ────────────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def loaded_model():
    """Load the serialised model once for the entire test module."""
    assert os.path.exists(MODEL_PATH), (
        f"Model file '{MODEL_PATH}' not found. Run train.py first."
    )
    return joblib.load(MODEL_PATH)


@pytest.fixture(scope="module")
def iris_test_split():
    """Return the same deterministic train/test split used in train.py."""
    iris = load_iris()
    _, X_test, _, y_test = train_test_split(
        iris.data, iris.target, test_size=0.2, random_state=42
    )
    return X_test, y_test


# ─── Test 1: Model file existence ────────────────────────────────────────────

def test_model_file_exists():
    """The model file must be present on disk after training."""
    assert os.path.exists(MODEL_PATH), (
        f"Expected model file '{MODEL_PATH}' was not found."
    )


# ─── Test 2: Prediction sanity check ─────────────────────────────────────────

def test_prediction_works(loaded_model):
    """The model must return a single integer class index for a valid input."""
    # A typical Setosa sample: sepal 5.1 cm, 3.5 cm | petal 1.4 cm, 0.2 cm
    sample = np.array([[5.1, 3.5, 1.4, 0.2]])
    prediction = loaded_model.predict(sample)

    # Output must be a 1-element array containing 0, 1, or 2
    assert len(prediction) == 1, "Prediction must return exactly one label."
    assert prediction[0] in {0, 1, 2}, (
        f"Prediction {prediction[0]} is not a valid class index (0, 1, or 2)."
    )


# ─── Test 3: Model accuracy threshold ────────────────────────────────────────

def test_model_accuracy(loaded_model, iris_test_split):
    """Accuracy on the held-out test set must be at least 90 %."""
    X_test, y_test = iris_test_split
    y_pred = loaded_model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    print(f"\n  [Test] Model accuracy: {accuracy * 100:.2f}%")
    assert accuracy >= 0.90, (
        f"Model accuracy {accuracy * 100:.2f}% is below the required 90 % threshold."
    )
