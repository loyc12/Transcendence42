# Generated by Django 4.2.7 on 2023-11-29 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='started_at',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
    ]