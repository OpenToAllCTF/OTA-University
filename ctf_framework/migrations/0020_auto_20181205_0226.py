# Generated by Django 2.0.1 on 2018-12-05 02:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ctf_framework', '0019_auto_20181204_2346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ctf_framework.Category'),
        ),
    ]