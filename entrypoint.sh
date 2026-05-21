#!/bin/bash
set -e

echo "Running migrations..."
python manage.py migrate --noinput 2>&1 || {
    echo "Faking all migrations (existing database)..."
    python manage.py migrate --fake --noinput
    python manage.py migrate --noinput
}
echo "Seeding catalog and config data..."
python manage.py seed_data --no-color

echo "Starting Gunicorn..."
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 4 --access-logfile -
