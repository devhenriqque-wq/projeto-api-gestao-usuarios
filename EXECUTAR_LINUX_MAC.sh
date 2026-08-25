#!/usr/bin/env bash
set -e

if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi

source .venv/bin/activate
python -m pip install -r requirements.txt

echo "Interface: http://127.0.0.1:8000"
echo "Swagger:   http://127.0.0.1:8000/docs"

python -m uvicorn app.main:app --reload
