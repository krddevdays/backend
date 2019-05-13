#!/bin/sh

echo "Apply database migration"
python3 manage.py migrate --noinput

echo "Starting server"
gunicorn krddevdays.wsgi:application --bind 0.0.0.0:8000 --timeout 60
