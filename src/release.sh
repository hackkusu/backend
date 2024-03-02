#!/bin/bash

#python manage.py makemigrations polls

python manage.py migrate

#python manage.py loaddata superuser.json # <-- todo later

#python manage.py createsuperuser --username superadmin --email admin@gfic.io --noinput || true
#python manage.py collectstatic --noinput
