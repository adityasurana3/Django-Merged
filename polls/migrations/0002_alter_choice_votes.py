# Generated by Django 4.0.1 on 2022-01-24 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choice',
            name='votes',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
