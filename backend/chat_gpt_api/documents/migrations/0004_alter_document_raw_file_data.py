# Generated by Django 4.2 on 2023-04-14 12:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("documents", "0003_rename_file_document_raw_file_data_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="document",
            name="raw_file_data",
            field=models.TextField(verbose_name="Documento anexado"),
        ),
    ]