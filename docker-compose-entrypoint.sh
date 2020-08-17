#!/bin/bash

until psql $DATABASE_URL -c '\l'; do
    >&2 echo "Posgres is unavailable - sleeping."
done

python3 /noter-backend/noter_backend/manage.py makemigrations  --settings=noter_backend.dev_settings
python3 /noter-backend/noter_backend/manage.py migrate --settings=noter_backend.dev_settings
python3 /noter-backend/noter_backend/manage.py shell --settings=noter_backend.dev_settings -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'dontusethispassword')"
python3 /noter-backend/noter_backend/manage.py runserver 0.0.0.0:3001 --settings=noter_backend.dev_settings

exec "$@"
