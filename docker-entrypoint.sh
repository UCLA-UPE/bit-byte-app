#!/bin/bash

# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

# Populate database with packaged data
# echo "Load packaged database dump"
# wiki for Bit-Byte challenge
# python manage.py loaddata wiki.json

# Start server
echo "Starting server"
python manage.py runserver 0.0.0.0:8000
