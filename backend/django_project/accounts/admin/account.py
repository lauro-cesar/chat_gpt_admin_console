from django.contrib import admin
from django.core.cache import cache
from django.utils.safestring import mark_safe
from project.celery_tasks import app
from django.contrib import messages
import base64
from django.utils.translation import gettext_lazy as _
from project.admin import ProjectBaseModelAdmin as BaseModelAdmin
from django.contrib.auth import get_user_model
from project.admin import dashboard_sites, admin_sites
from django.contrib.auth.admin import UserAdmin, GroupAdmin

Account = get_user_model()


class AccountAdmin(BaseModelAdmin,UserAdmin):
    save_on_top = True
    ordering = Account.ADMIN_ORDERING
    list_display = Account.ADMIN_LIST_DISPLAY
    list_filter = Account.ADMIN_LIST_FILTER
    search_fields = Account.ADMIN_SEARCH_FILTER
    list_editable = Account.ADMIN_LIST_EDITABLE
    list_display_links = Account.ADMIN_DISPLAY_LINKS
    filter_horizontal = Account.ADMIN_FILTER_HORIZONTAL
    def has_delete_permission(self, request, obj=None):
        return False
    def get_form(self, request, obj=None, **kwargs):
        defaults = {}
        if obj is None:
            defaults["form"] = self.add_form
        form = super().get_form(request, obj, **defaults)

        return form

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets

        if True in [request.user.is_operator, request.user.is_rootuser]:
            return (
                (None, {"fields": ("username", "password")}),
                (
                    _("Personal info"),
                    {"fields": ("first_name", "last_name", "email","privilege_level")},
                ),
                (
                    _("Permissions"),
                    {
                        "fields": (
                            "is_active",
                            "is_staff",
                            "groups",
                            "user_permissions",
                        ),
                    },
                ),
                (_("Important dates"), {"fields": ("last_login", "date_joined")}),
            )

        if request.user.is_superuser:
            return (
                (None, {"fields": ("username", "password")}),
                (
                    _("Personal info"),
                    {"fields": ("first_name", "last_name", "email")},
                ),
                (
                    _("Permissions"),
                    {
                        "fields": (
                            "is_active",
                            "is_staff",
                            "is_superuser",
                            "groups",
                            "user_permissions",
                        ),
                    },
                ),
                (_("Important dates"), {"fields": ("last_login", "date_joined")}),
            )

        return (
            (None, {"fields": ("username", "password")}),
            (
                _("Personal info"),
                {"fields": ("first_name", "last_name", "email", "avatar")},
            ),
        )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2"),
            },
        ),
    )


for admin_site in admin_sites:
    admin_site.register(Account, AccountAdmin)

for developer_site in dashboard_sites:
    developer_site.register(Account, AccountAdmin)
