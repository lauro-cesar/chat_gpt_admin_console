from django.conf import settings
import os
import sys
import re
from string import Template
from django.utils.module_loading import import_string
from django.apps import apps
from django.core.management.base import BaseCommand, CommandError, no_translations
from jinja2 import Template
from jinja2 import Markup
from project.models import BaseModel
from django.forms.models import model_to_dict
import copy
from . import _private as templates

import logging
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Update All models defaults"
    app_label = ""
    model_name = ""
    verbose_name = ""
    verbose_name_plural = ""
    render_context = {}
    base_dir = "/"
    save_to = "/"
    app_version = "v1"

    def add_arguments(self, parser):
        parser.add_argument("app_label", type=str)
        parser.add_argument("app_version", type=str)

    @property
    def log_output(self):
        return self.stdout

    def log(self, msg):
        self.log_output.write(msg)

    def create_file(self, base_dir, save_to, template_in, init_in):
        if not os.path.exists(f"{base_dir}"):
            os.makedirs(base_dir)

        template_output = Template(template_in).render(self.render_context)
        output = f"{base_dir}/{save_to}.py"
        init_file = f"{base_dir}/__init__.py"

        if not os.path.exists(f"{output}"):
            with open(output, "w") as save_to_file:
                save_to_file.write(template_output)
                save_to_file.close()

            init_out = Template(init_in).render(self.render_context)

            with open(init_file, "a") as init:
                init.write(init_out)
                init.close()

            self.stdout.write(self.style.SUCCESS(f"{output} criado com sucesso"))
        else:
            self.stdout.write(self.style.NOTICE(f"{output} Existe".upper()))

    def handle(self, *args, **options):
        self.app_version = options.get("app_version")
        self.app_label = options.get("app_label")

        apps_to_parse = []
        try:
            app = apps.get_app_config(self.app_label)
        except LookupError as err:
            logger.error(err.__repr__())
            self.stdout.write(self.style.ERROR(f"{self.app_label} Not Found"))
        else:
            apps_to_parse.append(app)

        modelos = [
            {
                "modulo": "models",
                "template_in": templates.MODEL_TEMPLATE,
                "init_in": templates.MODEL_INIT_TEMPLATE,
            },
            {
                "modulo": "tasks",
                "template_in": templates.TASK_TEMPLATE,
                "init_in": templates.TASK_INIT_TEMPLATE,
            },
            {
                "modulo": "signals",
                "template_in": templates.SIGNAL_TEMPLATE,
                "init_in": templates.SIGNAL_INIT_TEMPLATE,
            },
            {
                "modulo": "views",
                "template_in": templates.VIEW_TEMPLATE,
                "init_in": templates.VIEW_INIT_TEMPLATE,
            },
            {
                "modulo": "admin",
                "template_in": templates.ADMIN_TEMPLATE,
                "init_in": templates.ADMIN_INIT_TEMPLATE,
            },
            {
                "modulo": "serializers",
                "template_in": templates.SERIALIZER_TEMPLATE,
                "init_in": templates.SERIALIZER_INIT_TEMPLATE,
            },
            {
                "modulo": "consumers",
                "template_in": templates.CHANNELS_TEMPLATE,
                "init_in": templates.CHANNELS_INIT_TEMPLATE,
            },
            {
                "modulo": f"web_routes/{self.app_version}",
                "template_in": templates.WEB_URLS_TEMPLATE,
                "init_in": templates.WEB_URLS_INIT_TEMPLATE,
            },
            {
                "modulo": f"async_routes/{self.app_version}",
                "template_in": templates.ASYNC_URLS_TEMPLATE,
                "init_in": templates.ASYNC_URLS_INIT_TEMPLATE,
            },
            {
                "modulo": f"app_routes/{self.app_version}",
                "template_in": templates.APP_URLS_TEMPLATE,
                "init_in": templates.APP_URLS_INIT_TEMPLATE,
            },
            {
                "modulo": f"rest_routes/{self.app_version}",
                "template_in": templates.REST_URLS_TEMPLATE,
                "init_in": templates.REST_URLS_INIT_TEMPLATE,
            },
        ]

        for app in apps_to_parse:
            base_dir = getattr(app, "path", "/tmp/")
            models = app.get_models()
            for model in models:
                i = model()
                if not os.path.exists(f"{base_dir}"):
                    os.makedirs(base_dir)
                else:
                    self.stdout.write(self.style.SUCCESS(f" Base Dir Existe : {base_dir}"))

                if os.path.exists(f"{base_dir}"):
                    for modelo in modelos:
                        app_name = getattr(app, "name", "_")

                        self.render_context.update(
                            {
                                "app_name": app_name,
                                "app_version": self.app_version,
                                "STREAM_OBJECT_TASK_NAME": f"stream_live_update_{i.model_name}",
                                "STREAM_COLLECTION_TASK_NAME": f"{app_name}_collection_{i.model_name}",
                                "model_name": i.__class__.__name__,
                                "verbose_name_plural": i.getMeta.verbose_name_plural,
                                "verbose_name": i.getMeta.verbose_name,
                                "save_to": i.__module__.split('.')[-1],
                            }
                        )

                        self.create_file(
                            base_dir=f"{base_dir}/{modelo['modulo']}",
                            save_to=i.__module__.split('.')[-1],
                            template_in=modelo["template_in"],
                            init_in=modelo["init_in"],
                        )
