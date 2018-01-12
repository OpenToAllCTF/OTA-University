To get running:

- Install dependencies
- cd ota_university/

For Empty Database:
- python manage.py makemigrations
- python manage.py makemigrations ctf_framework
- python manage.py migrate
- python manage.py runserver

or drop a pre-made "db.sqlite3" into ota_university/



To create new admin accounts:
python manage.py createsuperuser
