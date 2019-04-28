#!/bin/sh

echo "Apply database migration"
python3 manage.py migrate --noinput

echo "Starting server"
python3 manage.py runserver 0.0.0.0:8000
