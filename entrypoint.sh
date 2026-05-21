#!/bin/bash
set -e

echo "Creating database schemas if they don't exist..."
python -c "
import django; django.setup()
from django.db import connection
SCHEMAS = ['catalog', 'core', 'transactions', 'audit', 'system']
with connection.cursor() as c:
    for schema in SCHEMAS:
        c.execute(f'CREATE SCHEMA IF NOT EXISTS {schema}')
print('Schemas created successfully')
"

echo "Running migrations..."
python manage.py migrate --noinput

echo "Seeding catalog and config data..."
python manage.py seed_data --no-color

echo "Starting Gunicorn..."
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 4 --access-logfile -
