from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import os
import sys
import re
from jinja2 import Template
from jinja2 import Markup
import logging
logger = logging.getLogger(__name__)

from ._private import (
    APP_URLS_TEMPLATE,
    APP_URLS_INIT_TEMPLATE,
    ADMIN_INIT_TEMPLATE,
    ADMIN_TEMPLATE,
    CHANNELS_TEMPLATE,
    CHANNELS_INIT_TEMPLATE,
    MODEL_TEMPLATE,
    TASK_TEMPLATE,
    VIEW_TEMPLATE,
    SIGNAL_TEMPLATE,
    SERIALIZER_TEMPLATE,
    MODEL_INIT_TEMPLATE,
    SIGNAL_INIT_TEMPLATE,
    VIEW_INIT_TEMPLATE,
    TASK_INIT_TEMPLATE,
    SERIALIZER_INIT_TEMPLATE,
    WEB_URLS_TEMPLATE,
    WEB_URLS_INIT_TEMPLATE,
    ASYNC_URLS_INIT_TEMPLATE,
    ASYNC_URLS_TEMPLATE,
    REST_URLS_INIT_TEMPLATE,
    REST_URLS_TEMPLATE,
)


class Command(BaseCommand):
    help = "Create a new model"
    app_name = ""
    model_name = ""
    verbose_name = "Verbose name"
    verbose_name_plural = "Verbose name Plural"
    render_context = {}
    base_dir = "/"
    save_to = "/"

    def add_arguments(self, parser):
        parser.add_argument("app_name", type=str)
        parser.add_argument("app_version", type=str)
        parser.add_argument("model_name", type=str)
        parser.add_argument("save_to", type=str)
        parser.add_argument("verbose_name", type=str)
        parser.add_argument("verbose_name_plural", type=str)

        parser.add_argument(
            "--save",
            action="store_true",
            help="Salvar bk se existir",
        )

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
        self.app_name = options.get("app_name")
        self.model_name = options.get("model_name")
        self.save_to = options.get("save_to")
        self.verbose_name = options.get("verbose_name")
        self.verbose_name_plural = options.get("verbose_name_plural")
        self.base_dir = f"{settings.BASE_DIR}/{self.app_name}"

        self.render_context.update(
            {
                "app_name": self.app_name,
                "app_version": self.app_version,
                "model_name": self.model_name,
                "verbose_name_plural": self.verbose_name_plural,
                "verbose_name": self.verbose_name,
                "save_to": self.save_to,
            }
        )

        modelos = [
            {
                "modulo": "models",
                "template_in": MODEL_TEMPLATE,
                "init_in": MODEL_INIT_TEMPLATE,
            },
            {
                "modulo": "tasks",
                "template_in": TASK_TEMPLATE,
                "init_in": TASK_INIT_TEMPLATE,
            },
            {
                "modulo": "signals",
                "template_in": SIGNAL_TEMPLATE,
                "init_in": SIGNAL_INIT_TEMPLATE,
            },
            {
                "modulo": "views",
                "template_in": VIEW_TEMPLATE,
                "init_in": VIEW_INIT_TEMPLATE,
            },
            {
                "modulo": "admin",
                "template_in": ADMIN_TEMPLATE,
                "init_in": ADMIN_INIT_TEMPLATE,
            },
            {
                "modulo": "serializers",
                "template_in": SERIALIZER_TEMPLATE,
                "init_in": SERIALIZER_INIT_TEMPLATE,
            },
            {
                "modulo": "consumers",
                "template_in": CHANNELS_TEMPLATE,
                "init_in": CHANNELS_INIT_TEMPLATE,
            },
            {
                "modulo": f"web_routes/{self.app_version}",
                "template_in": WEB_URLS_TEMPLATE,
                "init_in": WEB_URLS_INIT_TEMPLATE,
            },
            {
                "modulo": f"async_routes/{self.app_version}",
                "template_in": ASYNC_URLS_TEMPLATE,
                "init_in": ASYNC_URLS_INIT_TEMPLATE,
            },
            {
                "modulo": f"app_routes/{self.app_version}",
                "template_in": APP_URLS_TEMPLATE,
                "init_in": APP_URLS_INIT_TEMPLATE,
            },
            {
                "modulo": f"rest_routes/{self.app_version}",
                "template_in": REST_URLS_TEMPLATE,
                "init_in": REST_URLS_INIT_TEMPLATE,
            },
        ]

        if not os.path.exists(f"{self.base_dir}"):
            os.makedirs(self.base_dir)

        if os.path.exists(f"{self.base_dir}"):
            for modelo in modelos:
                self.create_file(
                    base_dir=f"{self.base_dir}/{modelo['modulo']}",
                    save_to=self.save_to,
                    template_in=modelo["template_in"],
                    init_in=modelo["init_in"],
                )

            self.stdout.write(self.style.SUCCESS("Successfully"))
        else:
            self.stdout.write(self.style.WARNING("Erro"))
