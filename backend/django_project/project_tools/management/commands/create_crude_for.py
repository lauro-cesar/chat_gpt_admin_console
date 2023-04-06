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
    help = "Create Flutter Rest Crud"

    def add_arguments(self, parser):
        parser.add_argument("args", metavar="app_label", nargs="*")

    @property
    def log_output(self):
        return self.stdout

    def log(self, msg):
        self.log_output.write(msg)

    def create_base_flutter_app_path(self, app):
        app_path = getattr(app, "path", "/tmp/")
        base_dir = f"{app_path}/{app.name}_wall"
        paths = list(map(lambda p: f"{base_dir}/{p}", ["collections", "models"]))

        for path in paths:
            if not os.path.exists(path):
                self.stdout.write(self.style.SUCCESS(f"Criar path: {path}"))
                os.makedirs(path)
            else:
                self.stdout.write(self.style.SUCCESS(f"Path existe: {path}"))

    def create_flutter_app_state(self, app, model):
        pass

    def create_flutter_app_wall(self, app):
        pass

    def create_flutter_collection_state(self, contexto) -> str:
        collection_state_template = getattr(templates, "FLUTTER_COLLECTION_STATE_TEMPLATE", "")
        return Template(collection_state_template).render(contexto)

    def create_flutter_collection_state_provider(self, contexto) -> str:
        collection_state_template = getattr(templates, "FLUTTER_COLLECTION_STATE_PROVIDER_TEMPLATE", "")
        return Template(collection_state_template).render(contexto)

    def create_flutter_model_state_provider(self, contexto) -> str:
        collection_state_template = getattr(templates, "FLUTTER_MODEL_STATE_PROVIDER_TEMPLATE", "")
        return Template(collection_state_template).render(contexto)

    def create_flutter_model_state(self, contexto) -> str:
        collection_state_template = getattr(templates, "FLUTTER_MODEL_STATE_TEMPLATE", "")
        return Template(collection_state_template).render(contexto)

    def create_flutter_model_form(self,contexto) -> str:
        collection_state_template = getattr(templates, "FLUTTER_MODEL_FORM_TEMPLATE", "")
        return Template(collection_state_template).render(contexto)

    def create_flutter_model(self, app, model, contexto):
        model_state_template = getattr(templates, "FLUTTER_MODEL_STATE_TEMPLATE", "")
        campos = getattr(model, "SERIALIZABLES", [])
        tipos = getattr(model, "FLUTTER_TYPES", {})
        tipos.update(BaseModel.FLUTTER_TYPES)
        campos_state = ["\n"]
        models_imports = []
        tipos_primarios = ["int", "String", "double"]
        tipos_related = ["related"]
        tipos_related_many = ["related_many"]
        todos_os_tipos = tipos_related + tipos_related_many + tipos_primarios
        for campo in campos:
            tipo = tipos.get(campo, {"type": "String"}).get("type", "String")



            if tipo in tipos_primarios:
                campos_state.append(f"{tipo} get {campo} => record['{campo}'];\n")

            if tipo in tipos_related:
                related_model = tipos.get(campo, {}).get("related_model")
                campos_state.append(f"{related_model} get {campo}\n")


        contexto.update({
            "flutter_model_state_fields": "".join(campos_state)
        })
        output = Template(model_state_template).render(contexto)

    def create_flutter_app_wall_state(self, app, model, contexto):
        """
        cirurgias_state/
            cirurgia/
                cirurgias_state.dart # collection
                cirurgias_provider.dart
                cirurgia_state.dart
                cirurgia_provider.dart
            convenio/
                convenios_state.dart
                convenios_provider.dart
                convenio_state.dart
                convenio_provider.dart
        """
        app_path = getattr(app, "path", "/tmp/")
        base_dir = f"{app_path}/{app.name}_state"
        i = model()
        model_name = f"{i.__class__.__name__}"


        model_state_dart_file = f"{i.model_name.lower()}/{i.__module__.split('.')[-1]}_record_state.dart"
        model_provider_dart_file = f"{i.model_name.lower()}/{i.__module__.split('.')[-1]}_record_provider.dart"

        collection_state_dart_file = f"{i.model_name.lower()}/{model_name.lower()}_collection_state.dart"
        collection_provider_dart_file = f"{i.model_name.lower()}/{model_name.lower()}_collection_provider.dart"

        contexto.update({
            "app_name": app.name,
            "base_dir": base_dir,
            "app_path": app_path,
            "model_file_name":i.model_name,
            "model_dir": f"{i.__module__.split('.')[-1]}",
            "wall_dir": f"{app.name}_state",
            "model_state_dart_file": model_state_dart_file,
            "model_provider_dart_file": model_provider_dart_file,
            "collection_state_dart_file": collection_state_dart_file,
            "collection_provider_dart_file": collection_provider_dart_file,
        })


        paths = list(map(lambda p: f"{base_dir}/{p}", [i.model_name]))

        self.stdout.write(self.style.SUCCESS(f"Base Dir: {base_dir}"))

        for path in paths:
            if not os.path.exists(path):
                self.stdout.write(self.style.SUCCESS(f"Criar path: {path}"))
                os.makedirs(path)
            else:
                self.stdout.write(self.style.SUCCESS(f"Path existe: {path}"))


        with open(f"{base_dir}/{model_provider_dart_file}", "w") as provider_output:
            model_provider = self.create_flutter_model_state_provider(contexto)
            provider_output.write(model_provider)

        with open(f"{base_dir}/{model_state_dart_file}", "w") as output:
            model_state = self.create_flutter_model_state(contexto)
            output.write(model_state)

        with open(f"{base_dir}/{collection_provider_dart_file}", "w") as output:
            model_state = self.create_flutter_collection_state_provider(contexto)
            output.write(model_state)

        with open(f"{base_dir}/{collection_state_dart_file}", "w") as output:
            model_state = self.create_flutter_collection_state(contexto)
            output.write(model_state)


    def create_flutter_forms(self,app, model, contexto):
        pass

    def handle(self, *app_labels, **options):
        app_labels = set(app_labels)
        apps_to_parse = []

        for app_label in app_labels:
            try:
                app = apps.get_app_config(app_label)
            except LookupError as err:
                logger.error(err.__repr__())
                self.stdout.write(self.style.ERROR(f"{app_label} Not Found"))
            else:
                apps_to_parse.append(app)

        for app in apps_to_parse:
            # self.create_base_flutter_app_path(app)
            models = app.get_models()
            for model in models:
                meta = model().getMeta
                i = model()
                contexto = {
                    "modelFileName": f"{i.model_name}",
                    "modelName": f"{i.__class__.__name__}",
                    "defaultModelValues": "..nome='nome'",
                }
                self.create_flutter_app_wall_state(app, model, contexto)
                # self.create_flutter_collection_state(app, model, contexto)
