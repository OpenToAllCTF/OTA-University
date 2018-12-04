# Generated by Django 2.0.1 on 2018-12-03 23:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ctf_framework', '0016_auto_20181203_2236'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ChallengeSolve',
            new_name='Solve',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='completed_challenges',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='solved_challenges',
            field=models.ManyToManyField(through='ctf_framework.Solve', to='ctf_framework.Challenge'),
        ),
    ]
