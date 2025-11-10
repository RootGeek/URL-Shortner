#!/usr/bin/env bash
set -e

# LinkScope auto-setup & HTTPS start script
# Usage:
#   bash start.sh
#
# Macht:
#   - venv erstellen (falls nicht vorhanden)
#   - Dependencies installieren/aktualisieren
#   - selbstsigniertes Zertifikat erzeugen (falls nicht vorhanden)
#   - Server mit HTTPS starten (Standard-Port 8443)

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

PORT="${PORT:-8443}"
CERT_FILE="${CERT_FILE:-cert.pem}"
KEY_FILE="${KEY_FILE:-key.pem}"

# Check python3
if ! command -v python3 >/dev/null 2>&1; then
  echo "[LinkScope] Fehler: python3 nicht gefunden. Bitte zuerst installieren."
  exit 1
fi

# Create venv if missing
if [ ! -d ".venv" ]; then
  echo "[LinkScope] Erstelle Virtual Environment (.venv)..."
  python3 -m venv .venv
fi

# Activate venv
# shellcheck source=/dev/null
source .venv/bin/activate

# Upgrade pip & install requirements
echo "[LinkScope] Aktualisiere pip & installiere Dependencies..."
pip install --upgrade pip >/dev/null
pip install -r requirements.txt

# Generate self-signed certificate if missing
if [ ! -f "$CERT_FILE" ] || [ ! -f "$KEY_FILE" ]; then
  if ! command -v openssl >/dev/null 2>&1; then
    echo "[LinkScope] Fehler: openssl nicht gefunden. Bitte installieren:"
    echo "  apt install -y openssl"
    exit 1
  fi
  echo "[LinkScope] Erzeuge selbstsigniertes TLS-Zertifikat (${CERT_FILE}, ${KEY_FILE})..."
  openssl req -x509 -newkey rsa:4096 -keyout "$KEY_FILE" -out "$CERT_FILE" -days 3650 -nodes -subj "/CN=LinkScope"
fi

echo
echo "[LinkScope] Startet HTTPS-Server auf https://0.0.0.0:${PORT} ..."
echo "[LinkScope] Hinweis: Selbstsigniertes Zertifikat -> Browser zeigt Warnung (erwartet)."
echo "[LinkScope] Abbruch mit STRG+C."
echo

# Start Uvicorn with HTTPS
uvicorn app.main:app --host 0.0.0.0 --port "${PORT}" --ssl-keyfile "$KEY_FILE" --ssl-certfile "$CERT_FILE"
