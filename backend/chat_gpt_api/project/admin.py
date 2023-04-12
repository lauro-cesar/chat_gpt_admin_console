from django.contrib import admin
from django.conf import settings
from django.utils.translation import gettext as _, gettext_lazy
from datetime import datetime
from django.contrib.auth.models import Group
from django.contrib.flatpages.models import FlatPage
from django.contrib.sites.models import Site
from django.utils.text import capfirst
from django.urls import NoReverseMatch, Resolver404, resolve, reverse
from django.apps import apps


class ProjectBaseModelAdmin(admin.ModelAdmin):
    """
    This base model manager all Admin requests
    """

    def save_model(self, request, obj, form, change):
        """
        When called from AdminInterface, lets set some hidden properties
        """
        obj = obj.transformModel()

        if True in [hasattr(obj, "criado_por"), hasattr(obj, "belongs_to")]:
            if obj._state.adding:
                obj.criado_por = request.user
                obj.belongs_to = request.user

            obj.modificado_por = request.user
            obj.save()

    def get_queryset(self, request):
        """
        Return a QuerySet of all model instances that can be edited by the
        admin site. This is used by changelist_view.
        """
        qs = self.model._default_manager.get_queryset()

        if True not in [request.user.is_superuser, request.user.is_operator]:
            if hasattr(request,"criado_por"):
                qs = qs.filter(criado_por=request.user.id)
            
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs

    admin_priority = 20
    default_lon = -5372220.98
    default_lat = -2413950.78
    map_width = 800
    map_height = 600
    default_zoom = 8
    save_on_top = True
    date_hierarchy = "dateCreated"
    list_per_page = 15
    list_max_show_all = 50
    actions_on_bottom = True
    EXCLUDE_FROM_ADMIN = []
    exclude = [
        "criado_por",
        "modificado_por",
        "removido_por",
        "isRemoved",
        "isActive",
        "isDone",
        "belongs_to",
        "isComplete",
        "isPublic",
        "isProcessed",
    ]


class BaseModelAdminTabular(admin.TabularInline):
    """"""


class BaseProjectAdminSite(admin.AdminSite):
    def _build_app_dict(self, request, label=None):
        """
        Build the app dictionary. The optional `label` parameter filters models
        of a specific app.
        """
        app_dict = {}

        if label:
            models = {
                m: m_a
                for m, m_a in self._registry.items()
                if m._meta.app_label == label
            }
        else:
            models = self._registry

        for model, model_admin in models.items():
            app_label = model._meta.app_label

            has_module_perms = model_admin.has_module_permission(request)
            if not has_module_perms:
                continue

            perms = model_admin.get_model_perms(request)

            # Check whether user has any perm for this module.
            # If so, add the module to the model_list.
            if True not in perms.values():
                continue

            info = (app_label, model._meta.model_name)
            if not hasattr(model, "MODEL_LIST_ORDER_VALUE"):
                property_name = (
                    f"{model._meta.model_name}_MODEL_LIST_ORDER_VALUE".upper()
                )
                model.MODEL_LIST_ORDER_VALUE = getattr(settings, property_name, 1000)

            model_dict = {
                "model": model,
                "MODEL_LIST_ORDER_VALUE": model.MODEL_LIST_ORDER_VALUE,
                "name": capfirst(model._meta.verbose_name_plural),
                "object_name": model._meta.object_name,
                "perms": perms,
                "admin_url": None,
                "add_url": None,
            }
            if perms.get("change") or perms.get("view"):
                model_dict["view_only"] = not perms.get("change")
                try:
                    model_dict["admin_url"] = reverse(
                        "admin:%s_%s_changelist" % info, current_app=self.name
                    )
                except NoReverseMatch:
                    pass
            if perms.get("add"):
                try:
                    model_dict["add_url"] = reverse(
                        "admin:%s_%s_add" % info, current_app=self.name
                    )
                except NoReverseMatch:
                    pass

            if app_label in app_dict:
                app_dict[app_label]["models"].append(model_dict)
            else:
                if not hasattr(apps.get_app_config(app_label), "APP_LIST_ORDER_VALUE"):
                    property_name = f"{app_label}_APP_LIST_ORDER_VALUE".upper()
                    APP_LIST_ORDER_VALUE = getattr(settings, property_name, 1000)

                else:
                    APP_LIST_ORDER_VALUE = apps.get_app_config(
                        app_label
                    ).APP_LIST_ORDER_VALUE

                app_dict[app_label] = {
                    "name": apps.get_app_config(app_label).verbose_name,
                    "app_label": app_label,
                    "APP_LIST_ORDER_VALUE": APP_LIST_ORDER_VALUE,
                    "app_url": reverse(
                        "admin:app_list",
                        kwargs={"app_label": app_label},
                        current_app=self.name,
                    ),
                    "has_module_perms": has_module_perms,
                    "models": [model_dict],
                }

        return app_dict

    def get_app_list(self, request, app_label=None):
        """
        Return a sorted list of all the installed apps that have been
        registered in this site.
        """
        app_dict = self._build_app_dict(request, app_label)

        # Sort the apps by order value.
        app_list = sorted(
            app_dict.values(),
            key=lambda x: x.get(
                "APP_LIST_ORDER_VALUE", f"{settings.DEFAULT_APP_ORDER_VALUE}"
            ),
        )

        # Sort the models by order value within each app.
        for app in app_list:
            app["models"].sort(
                key=lambda x: x.get(
                    "MODEL_LIST_ORDER_VALUE", f"{settings.DEFAULT_MODEL_ORDER_VALUE}"
                )
            )
        return app_list


class ProjectAdminSite(BaseProjectAdminSite):
    """
    AdminSite for admin console
    """

    site_header = _(f"{settings.SITE_HEADER}")
    site_title = _(f"{settings.SITE_TITLE}")
    index_title = _(f"{settings.SITE_INDEX_TITLE}")
    enable_nav_sidebar = True

    def each_context(self, request):
        """
        Lets Inject some required properties to context
        """
        self.request = request
        contexto = super().each_context(request)
        contexto.update(
            {
                "admin_path": "admin",
                "rest_api_address": f"{settings.REST_API_ADDRESS}",
                "socket_api_address": f"{settings.SOCKET_API_ADDRESS}",
            }
        )
        return contexto


project_admin_site = ProjectAdminSite(name="admin-console")


class FlatPageModelAdmin(admin.ModelAdmin):
    filter_horizontal = ["sites"]


class GroupModelAdmin(admin.ModelAdmin):
    filter_horizontal = ["permissions"]


project_admin_site.register(Site)
project_admin_site.register(Group, GroupModelAdmin)
project_admin_site.register(FlatPage, FlatPageModelAdmin)


class ProjectDashboardSite(BaseProjectAdminSite):
    """
    Admin Site for dashboard console
    """

    site_header = _(f"{settings.SITE_HEADER}")
    site_title = _(f"{settings.SITE_TITLE}")
    index_title = _(f"{settings.SITE_INDEX_TITLE}")
    enable_nav_sidebar = True

    # index_template = "admin/admin_dashboard/index.html"
    # app_index_template = "admin/admin_dashboard/app_index.html"

    def each_context(self, request):
        """
        Lets Inject some required properties to context
        """
        self.request = request
        contexto = super().each_context(request)
        contexto.update(
            {
                "admin_path": "dashboard",
                "rest_api_address": f"{settings.REST_API_ADDRESS}",
                "socket_api_address": f"{settings.SOCKET_API_ADDRESS}",
            }
        )
        return contexto


project_dashboard_site = ProjectDashboardSite(name="admin-dashboard")

admin_sites = [project_admin_site, admin.site]
dashboard_sites = [project_dashboard_site]
