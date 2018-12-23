# OTA University

OTA University is a training ground for OTA members.
Members register via their Slack account and participate in
solving and creating challenges for the OTA community.

Based on the amount of _currently active_ challenges solved,
members gain points and ranks.

# Requirements
The web application runs on Python3 and uses Slack as an
authentication service.

To use OTA-University on your Slack, you'll need to create a
Slack Application and fetch its `SLACK_CLIENT_ID` and `SLACK_CLIENT_SECRET`.
More information [here](https://api.slack.com/applications).

# Deployment
- `git clone https://github.com/OpenToAllCTF/OTA-University`
- `cd OTA-University`
- `pip3 install -r REQUIREMENTS.txt`
- `cp ota_university/config.yaml.template ota_university/config.yaml`
- Fill in the settings in ota_university/config.yml
- `python3 manage.py migrate`
- `python3 manage.py runserver`

# Seeding database

The database can be seeded with default values through the `ctf_framework/fixtures/dev.yaml` file.

To do so, use the following command : `python3 manage.py loaddata dev`

# Becoming an admin

To become an admin of OTA University, you need to set your User object's `is_staff` property to `True`. You can do this via the `manage.py shell` command :

```
$ python3 manage.py shell
Python 3.7.0 (default, Dec 15 2018, 22:16:40)
[Clang 10.0.0 (clang-1000.10.44.4)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>> from ctf_framework.models import User
>>> user = User.objects.first()
>>> user.is_staff = True
>>> user.save()
```

# Faking challenge solves

You can manipulate the database easily via `manage.py shell`. For example, in order to
add solves to a challenge, we can manually create `Solve` objects and link them to your account :

```
$ python3 manage.py shell
Python 3.7.0 (default, Dec 15 2018, 22:16:40)
[Clang 10.0.0 (clang-1000.10.44.4)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>> from ctf_framework.models import Solve, Challenge
>>> challenge = Challenge.objects.first()
>>> [Solve.objects.create(user_id=1, challenge=challenge) for i in range(0x20)]
```
