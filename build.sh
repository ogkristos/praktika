#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
python -c "
from django.contrib.auth.models import User
try:
    User.objects.create_superuser('admin', 'admin@example.com', 'Admin123!')
    print('Superuser created')
except:
    print('Superuser already exists')
"
