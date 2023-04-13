# Generated by Django 4.2 on 2023-04-13 04:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Organization",
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
                    "organization_name",
                    models.CharField(
                        max_length=256, verbose_name="Nome da organização"
                    ),
                ),
                (
                    "chatgpt_api_token",
                    models.CharField(max_length=512, verbose_name="Token da API"),
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
                "verbose_name": "Organização",
                "verbose_name_plural": "Organizações",
                "ordering": ["lastModified"],
                "abstract": False,
            },
        ),
    ]
