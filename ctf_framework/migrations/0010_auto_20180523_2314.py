# Generated by Django 2.0.1 on 2018-05-23 23:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ctf_framework', '0009_userprofile_completed_challenges'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TitleGranted',
            new_name='TitleGrant',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='earned_titles',
            field=models.ManyToManyField(through='ctf_framework.TitleGrant', to='ctf_framework.Title'),
        ),
    ]