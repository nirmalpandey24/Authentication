# Generated by Django 5.0.4 on 2024-05-18 10:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_usertoken'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserToken',
        ),
    ]
