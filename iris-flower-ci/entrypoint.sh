#!/bin/bash
# =============================================================================
# entrypoint.sh — Container entry point for the Iris Flower ML pipeline
# =============================================================================
# Execution order:
#   1. Train the Logistic Regression model → writes iris_model.pkl
#   2. Run inference on sample inputs      → reads iris_model.pkl
#
# 'set -e' makes the script exit immediately if any command returns a non-zero
# exit code. Without it, a failing train.py would silently let predict.py
# run (and crash), making errors much harder to diagnose.
# =============================================================================
set -e

echo "=================================================="
echo "   Iris Flower ML Pipeline — Container Starting"
echo "   Python: $(python --version 2>&1)"
echo "   Date  : $(date -u '+%Y-%m-%d %H:%M:%S UTC')"
echo "=================================================="

# ── Step 1: Train the model ────────────────────────────────────────────────
echo ""
echo ">>> [1/2] Training the Logistic Regression model..."
echo "--------------------------------------------------"
python train.py

# ── Step 2: Run predictions ────────────────────────────────────────────────
echo ""
echo ">>> [2/2] Running predictions on sample inputs..."
echo "--------------------------------------------------"
python predict.py

# ── Done ───────────────────────────────────────────────────────────────────
echo ""
echo "=================================================="
echo "   Pipeline complete — container exiting cleanly."
echo "=================================================="
