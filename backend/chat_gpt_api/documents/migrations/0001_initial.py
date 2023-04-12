# Generated by Django 4.2 on 2023-04-12 01:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("organizations", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
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
                ("isIndexed", models.BooleanField(default=False)),
                ("inProgress", models.BooleanField(default=False)),
                (
                    "document_file",
                    models.FileField(upload_to="", verbose_name="Documento anexado"),
                ),
                ("metadata", models.JSONField(blank=True, default=dict, null=True)),
                (
                    "belongs_to",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="belongs_to_%(app_label)s_%(class)s_related",
                        related_query_name="belongs_to_%(app_label)s_%(class)ss",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "criado_por",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="criado_por_%(app_label)s_%(class)s_related",
                        related_query_name="criado_por_%(app_label)s_%(class)ss",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "modificado_por",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="modificado_por_%(app_label)s_%(class)s_related",
                        related_query_name="modificado_por_%(app_label)s_%(class)ss",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
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
                (
                    "removido_por",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="removido_por_%(app_label)s_%(class)s_related",
                        related_query_name="removido_por_%(app_label)s_%(class)ss",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Documento",
                "verbose_name_plural": "Documentos",
                "ordering": ["lastModified"],
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Embedding",
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
                ("isIndexed", models.BooleanField(default=False)),
                ("inProgress", models.BooleanField(default=False)),
                ("isReadyForIndex", models.BooleanField(default=False)),
                ("embedding_raw_content", models.TextField()),
                ("generated_embedding", models.JSONField(default=dict)),
                (
                    "num_tokens",
                    models.PositiveSmallIntegerField(
                        default=0, verbose_name="Total de tokens"
                    ),
                ),
                (
                    "document_page",
                    models.PositiveSmallIntegerField(
                        default=1, verbose_name="Página correspondente"
                    ),
                ),
                (
                    "belongs_to",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="belongs_to_%(app_label)s_%(class)s_related",
                        related_query_name="belongs_to_%(app_label)s_%(class)ss",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "criado_por",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="criado_por_%(app_label)s_%(class)s_related",
                        related_query_name="criado_por_%(app_label)s_%(class)ss",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "document",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="document_embeddings",
                        to="documents.document",
                        verbose_name="Documento",
                    ),
                ),
                (
                    "modificado_por",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="modificado_por_%(app_label)s_%(class)s_related",
                        related_query_name="modificado_por_%(app_label)s_%(class)ss",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "removido_por",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="removido_por_%(app_label)s_%(class)s_related",
                        related_query_name="removido_por_%(app_label)s_%(class)ss",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Raw embedding chunk",
                "verbose_name_plural": "Raw embeddings chunks",
                "ordering": ["lastModified"],
                "abstract": False,
            },
        ),
    ]
