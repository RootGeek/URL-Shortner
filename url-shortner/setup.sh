#!/usr/bin/env bash
set -e

# Simple helper to setup venv and install dependencies on Ubuntu-like systems.

if [ ! -f "requirements.txt" ]; then
  echo "Bitte im Projektordner ausführen, wo requirements.txt liegt."
  exit 1
fi

echo "[LinkScope] Erstelle Virtual Environment (.venv)..."
python3 -m venv .venv

echo "[LinkScope] Aktiviere Virtual Environment und installiere Dependencies..."
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo
echo "[LinkScope] Setup fertig."
echo "Starte die Anwendung mit:"
echo "  source .venv/bin/activate"
echo "  uvicorn app.main:app --host 0.0.0.0 --port 8000"
