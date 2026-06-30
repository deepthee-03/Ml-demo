# =============================================================================
# train.py — Train a Logistic Regression model on the Iris dataset
# =============================================================================
# This script:
#   1. Loads the built-in Iris dataset from scikit-learn
#   2. Splits it into training and test sets
#   3. Trains a Logistic Regression classifier
#   4. Evaluates the model (accuracy, confusion matrix, classification report)
#   5. Saves the trained model to iris_model.pkl via joblib
# =============================================================================

import joblib
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split

# ── 1. Load the Iris dataset ──────────────────────────────────────────────────
iris = load_iris()
X = iris.data          # Features: sepal/petal length & width
y = iris.target        # Labels : 0=setosa, 1=versicolor, 2=virginica

# ── 2. Split into training (80 %) and test (20 %) sets ────────────────────────
# random_state=42 makes the split reproducible across runs
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ── 3. Train a Logistic Regression classifier ─────────────────────────────────
# max_iter=200 gives the solver enough iterations to converge on this dataset
model = LogisticRegression(max_iter=200, random_state=42)
model.fit(X_train, y_train)

# ── 4. Make predictions on the test set ──────────────────────────────────────
y_pred = model.predict(X_test)

# ── 5. Evaluate the model ─────────────────────────────────────────────────────
accuracy = accuracy_score(y_test, y_pred)

print("=" * 60)
print("          IRIS FLOWER CLASSIFICATION — RESULTS")
print("=" * 60)

print(f"\n  Accuracy Score : {accuracy * 100:.2f}%")

print("\n  Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("\n  Classification Report:")
print(
    classification_report(y_test, y_pred, target_names=iris.target_names)
)

# ── 6. Save the trained model to disk ─────────────────────────────────────────
model_path = "iris_model.pkl"
joblib.dump(model, model_path)
print(f"  Model saved to: {model_path}")
print("=" * 60)
