#! /usr/bin/env sh

echo "Apply database migration"
python3 manage.py migrate --noinput

if [ "$DEBUG" != "True" ]; then
    echo "Collect static"
    python3 manage.py collectstatic --noinput
fi