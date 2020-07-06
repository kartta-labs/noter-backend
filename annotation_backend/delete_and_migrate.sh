rm main/migrations/0*
rm db.sqlite3
./manage.py makemigrations
./manage.py migrate
./manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('sasantv', 'sasantv@google.com', '123')"
