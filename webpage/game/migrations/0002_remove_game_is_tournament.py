# Generated by Django 4.2.7 on 2023-12-16 20:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='is_tournament',
        ),
    ]
