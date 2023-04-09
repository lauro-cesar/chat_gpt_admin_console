# Generated by Django 4.2 on 2023-04-09 03:43

from django.db import migrations, models
import django.db.models.deletion
import project.models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("organizations", "__first__"),
    ]

    operations = [
        migrations.CreateModel(
            name="Document",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "dateCreated",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Data de criação"
                    ),
                ),
                (
                    "lastModified",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Última modificacao"
                    ),
                ),
                ("isActive", models.BooleanField(default=True, null=True)),
                ("isPublic", models.BooleanField(default=False, null=True)),
                ("isRemoved", models.BooleanField(default=False, null=True)),
                (
                    "document_name",
                    models.CharField(max_length=128, verbose_name="Nome do documento"),
                ),
                (
                    "num_tokens",
                    models.PositiveIntegerField(
                        default=0, verbose_name="Total de Tokens"
                    ),
                ),
                (
                    "document_file",
                    models.FileField(upload_to="", verbose_name="Documento anexado"),
                ),
                ("metadata", models.JSONField(blank=True, default=dict, null=True)),
                (
                    "organization",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="organization_docs",
                        to="organizations.organization",
                        verbose_name="Organização",
                    ),
                ),
            ],
            options={
                "verbose_name": "Documento",
                "verbose_name_plural": "Documentos",
                "ordering": ["lastModified"],
                "abstract": False,
            },
            bases=(models.Model, project.models.BaseModelForeignMixin),
        ),
    ]