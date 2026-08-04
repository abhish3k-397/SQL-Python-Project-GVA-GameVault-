#!/usr/bin/env bash
# Script to run GameVault Flask Backend & React Vite Bun Frontend concurrently

# Use virtualenv python if present
if [ -d ".venv" ]; then
  PYTHON_BIN=".venv/bin/python"
else
  PYTHON_BIN="python3"
fi

echo "🚀 Starting GameVault Python Flask API Backend..."
$PYTHON_BIN flask_app/app.py &
FLASK_PID=$!

echo "⚡ Starting GameVault React Bun + Vite Frontend..."
cd frontend
if command -v bun &> /dev/null; then
  bun run dev
else
  npm run dev
fi

kill $FLASK_PID

