#!/bin/sh

echo "Apply database migration"
python3 manage.py migrate --noinput

echo "Starting server"
gunicorn krddevdays.wsgi:application --bind 127.0.0.1:8000 --timeout 60
