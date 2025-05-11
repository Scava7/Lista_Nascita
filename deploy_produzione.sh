#!/bin/bash

# ===============================================
# Script di deploy per l'ambiente di produzione
# Uso:
#   ./deploy_prod.sh
# Assicurati che sia eseguibile con:
#   chmod +x deploy_prod.sh
# ===============================================

echo "Attivazione ambiente virtuale..."
source venv/bin/activate

echo "Aggiornamento pacchetti Python..."
pip install -r requirements.txt

echo "Applicazione migrazioni..."
python manage.py migrate

echo "Raccolta statici..."
python manage.py collectstatic --noinput

echo "Riavvio completato. Tutto aggiornato!"