from django.contrib.admin.apps import AdminConfig


class ProjectConfig(AdminConfig):
    default_auto_field = "django.db.models.AutoField"
    default_site = "project.admin.ProjectAdminSite"
