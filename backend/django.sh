#!/bin/sh

echo "start server"
python manage.py makemigrations car
python manage.py makemigrations authc
python manage.py migrate
python manage.py runserver 0.0.0.0:8000