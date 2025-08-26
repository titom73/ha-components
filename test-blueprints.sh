#!/bin/bash

# Blueprint Validation Test Script
# This script runs all validation tests locally before pushing to GitHub

set -e

echo "🧪 Blueprint Validation Test Suite"
echo "=================================="

# Check if we're in the right directory
if [ ! -d "blueprints" ]; then
    echo "❌ Error: blueprints directory not found. Run this script from the repository root."
    exit 1
fi

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "🔧 Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source .venv/bin/activate

# Set Python command to use venv
PYTHON_CMD=".venv/bin/python"

# Check if Python is available
if ! command -v "$PYTHON_CMD" &> /dev/null; then
    echo "❌ Error: Python 3 is required but not installed."
    exit 1
fi

echo "📦 Installing dependencies..."
$PYTHON_CMD -m pip install --quiet pyyaml yamllint

echo ""
echo "1️⃣  Testing YAML syntax..."
echo "=========================="

# Run yamllint if available
if command -v yamllint &> /dev/null; then
    yamllint blueprints/ || echo "⚠️  yamllint found issues (continuing...)"
else
    echo "⚠️  yamllint not available, skipping syntax check"
fi

echo ""
echo "2️⃣  Testing YAML structure..."
echo "============================="
$PYTHON_CMD .github/scripts/validate_yaml_structure.py

echo ""
echo "3️⃣  Testing blueprint schema..."
echo "==============================="
$PYTHON_CMD .github/scripts/validate_blueprint_schema.py

echo ""
echo "4️⃣  Testing blueprint imports..."
echo "==============================="
$PYTHON_CMD .github/scripts/test_blueprint_imports.py

echo ""
echo "5️⃣  Checking documentation sync..."
echo "=================================="
$PYTHON_CMD .github/scripts/check_docs_sync.py

echo ""
echo "✅ All tests completed!"
echo ""
echo "📋 Summary:"
echo "- YAML syntax validation"
echo "- Blueprint schema validation"
echo "- Import simulation test"
echo "- Documentation synchronization check"
echo ""
echo "🚀 Ready to push to GitHub!"
