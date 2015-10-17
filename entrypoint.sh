export DJANGO_SECRET_KEY=`python gen-secret.py`
export DATABASE_USER=hackor
export DATABASE_PASSWORD=hackor
python manage.py migrate
python manage.py runserver
