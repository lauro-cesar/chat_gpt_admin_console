# Generated by Django 4.2 on 2023-04-12 03:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("chats", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="question",
            name="isReady",
            field=models.BooleanField(default=False),
        ),
    ]
