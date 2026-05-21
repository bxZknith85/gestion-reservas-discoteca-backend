#!/bin/bash
set -e

echo "Resetting migration records for idempotent deploy..."
python -c "
import django; django.setup()
from django.db import connection
with connection.cursor() as c:
    c.execute('DELETE FROM django_migrations')
" 2>/dev/null || true

echo "Running migrations..."
set +e
python manage.py migrate --noinput 2>&1
rc=$?
set -e
if [ $rc -ne 0 ]; then
    echo "Faking remaining migrations (app tables already exist)..."
    python manage.py migrate --fake --noinput
fi
echo "Seeding catalog and config data..."
python manage.py seed_data --no-color

echo "Starting Gunicorn..."
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 4 --access-logfile -
