#!/bin/bash
cd "$(dirname "$0")"

# attiva il venv in modo portabile
source ./venv/bin/activate

# usa python3 per evitare problemi
python manage.py runserver 0.0.0.0:8000