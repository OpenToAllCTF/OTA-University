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

#Slack oAuth
Using https://github.com/izdi/django-slack-oauth

https://api.slack.com/slack-apps
- Create a Slack app
- Name it OTA University or something similar
- Set Workspace to OTA
- Click Permissions
- Add Redirect URL of {URL}/slack/login
- Under Scopes add: user.profile:read
- Select "Basic Information" on left
- Install Your App To Your Workspace (OTA)
- Add Client ID and Client Secret to settings.py


