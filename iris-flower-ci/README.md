# Iris Flower Classification — CI/CD with GitHub Actions

A beginner-friendly Machine Learning project that trains a **Logistic Regression** classifier on the classic **Iris flower dataset**, evaluates it with standard metrics, and runs the full training + testing pipeline automatically on every Git push via **GitHub Actions CI**.

---

## Project Overview

| Item | Detail |
|---|---|
| Dataset | Iris (built into scikit-learn — no download required) |
| Algorithm | Logistic Regression |
| Evaluation | Accuracy Score, Confusion Matrix, Classification Report |
| Persistence | Model saved as `iris_model.pkl` via `joblib` |
| Tests | 3 pytest unit tests (file exists, prediction works, accuracy ≥ 90 %) |
| CI Platform | GitHub Actions (Ubuntu, Python 3.11) |

### What the model predicts

Given four measurements of an Iris flower in centimetres the model outputs one of three species:

| Label | Species |
|---|---|
| 0 | *Iris setosa* |
| 1 | *Iris versicolor* |
| 2 | *Iris virginica* |

---

## Folder Structure

```
iris-flower-ci/
│
├── train.py          # Load data → train model → evaluate → save iris_model.pkl
├── predict.py        # Load iris_model.pkl → predict species for sample inputs
├── test_model.py     # pytest unit tests (3 tests)
├── requirements.txt  # All required Python libraries with pinned versions
├── README.md         # This file
├── iris_model.pkl    # Generated after you run train.py (not committed to Git)
└── .github/
    └── workflows/
        └── ci.yml    # GitHub Actions CI pipeline definition
```

---

## Prerequisites

- Python 3.11 or later
- pip (Python package manager)
- Git

---

## Installation

```bash
# 1. Clone the repository (or navigate to the project folder)
git clone https://github.com/<your-username>/iris-flower-ci.git
cd iris-flower-ci

# 2. (Recommended) Create and activate a virtual environment
python -m venv venv

# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# 3. Install all dependencies
pip install -r requirements.txt
```

---

## Running the Project Locally

### Step 1 — Train the model

```bash
python train.py
```

Expected output:

```
============================================================
          IRIS FLOWER CLASSIFICATION — RESULTS
============================================================

  Accuracy Score : 100.00%

  Confusion Matrix:
[[10  0  0]
 [ 0  9  0]
 [ 0  0 11]]

  Classification Report:
              precision    recall  f1-score   support
     setosa       1.00      1.00      1.00        10
 versicolor       1.00      1.00      1.00         9
  virginica       1.00      1.00      1.00        11
  ...
  Model saved to: iris_model.pkl
============================================================
```

### Step 2 — Predict flower species

```bash
python predict.py
```

Expected output:

```
Model loaded from: iris_model.pkl

============================================================
          IRIS FLOWER SPECIES PREDICTIONS
============================================================
  #    Input (cm)                           Predicted Species
  --------------------------------------------------------
  1    [5.1, 3.5, 1.4, 0.2]                Setosa
  2    [6.7, 3.0, 5.2, 2.3]                Virginica
  3    [5.9, 3.0, 4.2, 1.5]                Versicolor
============================================================
```

---

## Running Tests

```bash
pytest test_model.py -v -s
```

| Test | What it checks |
|---|---|
| `test_model_file_exists` | `iris_model.pkl` was created by `train.py` |
| `test_prediction_works` | Model returns a valid class index (0, 1, or 2) |
| `test_model_accuracy` | Model accuracy on test split is ≥ 90 % |

Expected output:

```
collected 3 items

test_model.py::test_model_file_exists PASSED
test_model.py::test_prediction_works  PASSED
test_model.py::test_model_accuracy    PASSED

============================================================ 3 passed in 0.42s ============================================================
```

---

## GitHub Actions CI Workflow

The workflow file is located at `.github/workflows/ci.yml`.

### What it does — step by step

```
Push / PR to main
       │
       ▼
┌─────────────────────────────────────┐
│ 1. Checkout repository              │  actions/checkout@v4
│ 2. Set up Python 3.11               │  actions/setup-python@v5
│ 3. Upgrade pip                      │  python -m pip install --upgrade pip
│ 4. Install requirements             │  pip install -r requirements.txt
│ 5. Train model  → iris_model.pkl    │  python train.py
│ 6. Run pytest  (3 tests)            │  pytest test_model.py -v -s
│ 7. Print PASSED / FAILED summary    │  always() step
└─────────────────────────────────────┘
```

### Triggers

| Event | Branch |
|---|---|
| `push` | `main` |
| `pull_request` | `main` |

You can view live run results in the **Actions** tab of your GitHub repository.

---

## How to Push to GitHub and Trigger CI

### 1 — Initialise a local Git repository

```bash
# Inside the iris-flower-ci/ folder
git init
git add .
git commit -m "feat: initial Iris classification project with CI"
```

> **Tip:** Add `iris_model.pkl` to `.gitignore` so the binary model file is not tracked:
> ```bash
> echo "iris_model.pkl" >> .gitignore
> git add .gitignore
> git commit -m "chore: ignore generated model file"
> ```

### 2 — Create a GitHub repository

1. Go to [github.com](https://github.com) and sign in.
2. Click **New repository**.
3. Name it `iris-flower-ci`, choose **Public** or **Private**, then click **Create repository**.
4. Do **not** initialise with a README (you already have one locally).

### 3 — Connect local repo to GitHub and push

```bash
# Replace <your-username> with your actual GitHub username
git remote add origin https://github.com/<your-username>/iris-flower-ci.git
git branch -M main
git push -u origin main
```

### 4 — Watch the CI pipeline run

1. Open your repository on GitHub.
2. Click the **Actions** tab.
3. You will see a workflow named **"Iris Flower CI Pipeline"** running automatically.
4. Click it to expand the live log for each step.
5. A green tick ✅ means all tests passed; a red cross ❌ means something failed — click the step to read the error.

Every subsequent `git push` to `main` (or any pull request targeting `main`) will trigger the pipeline again automatically.

---

## Key Libraries

| Library | Purpose |
|---|---|
| `scikit-learn` | Iris dataset, Logistic Regression, metrics |
| `joblib` | Efficient model serialisation (save/load `.pkl`) |
| `numpy` | Numerical array operations |
| `pytest` | Unit testing framework |

---

## License

This project is released under the [MIT License](https://opensource.org/licenses/MIT).
