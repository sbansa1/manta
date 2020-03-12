#!/bin/sh

echo "Connecting to PostGres...."

while ! nc -z event-db 5432;do
     sleep 1.0
done

echo "postgres stated....."

python manage.py run -h 0.0.0.0