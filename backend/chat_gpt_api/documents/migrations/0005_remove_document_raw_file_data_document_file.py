# Generated by Django 4.2 on 2023-04-14 12:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("documents", "0004_alter_document_raw_file_data"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="document",
            name="raw_file_data",
        ),
        migrations.AddField(
            model_name="document",
            name="file",
            field=models.FileField(
                default="", upload_to="", verbose_name="Documento anexado"
            ),
            preserve_default=False,
        ),
    ]
