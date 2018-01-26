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

# Creating an Administrator Account
To create new admin accounts, use the following command :
`python3 manage.py createsuperuser`

Visit `{URL}/admin` to login with the new account.
