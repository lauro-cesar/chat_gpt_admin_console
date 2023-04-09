"""
Copyright (c) 2023, Lauro Cesar <lauro@hostcert.com.br>
All rights reserved under BSD 3-Clause License.
"""

COPYRIGHT_HEADER="""
Copyright (c) 2023, Lauro Cesar <lauro@hostcert.com.br>
All rights reserved under BSD 3-Clause License.
"""

APP_URLS_TEMPLATE = """
\"\"\"
Copyright (c) 2023, Lauro Cesar <lauro@hostcert.com.br>
All rights reserved under BSD 3-Clause License.
\"\"\"
from django.urls import path,include, re_path
from {{app_name|lower}}.views import {{model_name}}TemplateView,{{model_name}}DetailView, {{model_name}}ListView, {{model_name}}UpdateView, {{model_name}}DeleteView, {{model_name}}CreateView

urlpatterns = [    
    path("", {{model_name}}TemplateView.as_view(template_name="{{model_name|lower}}/app_templates/{{app_version}}/{{model_name|lower}}_index.html"), name="{{model_name|lower}}-index"),
    path("collection/", {{model_name}}ListView.as_view(template_name = "{{model_name|lower}}/app_templates/{{app_version}}/{{model_name|lower}}_list.html"), name="{{model_name|lower}}-list"),
    path("collection/<int:pk>/", {{model_name}}DetailView.as_view(template_name = "{{model_name|lower}}/app_templates/{{app_version}}/{{model_name|lower}}_detail.html"), name='{{model_name|lower}}-detail'),
    path("collection/<int:pk>/editar/", {{model_name}}UpdateView.as_view(template_name = "{{model_name|lower}}/app_templates/{{app_version}}/{{model_name|lower}}_update.html"), name='{{model_name|lower}}-update'),
    path("collection/<int:pk>/remover/", {{model_name}}DeleteView.as_view(template_name = "{{model_name|lower}}/app_templates/{{app_version}}/{{model_name|lower}}_delete.html"), name='{{model_name|lower}}-delete'),    path("collection/adicionar/", {{model_name}}CreateView.as_view(template_name = "{{model_name|lower}}/app_templates/{{app_version}}/{{model_name|lower}}_create.html"), name='{{model_name|lower}}-create'),
]
"""
APP_URLS_INIT_TEMPLATE = """ """

ASYNC_URLS_TEMPLATE = """
\"\"\"
Copyright (c) 2023, Lauro Cesar <lauro@hostcert.com.br>
All rights reserved under BSD 3-Clause License.
\"\"\"
from django.urls import path
from {{app_name|lower}}.consumers import {{model_name}}Consumer, {{model_name}}CollectionConsumer, {{model_name}}CollectionIdOnlyConsumer

async_urlpatterns = [
    path(
        "channels/{{model_name|lower}}/collection/",
        {{model_name}}CollectionConsumer.as_asgi(),
    ),
    path(
        "channels/{{model_name|lower}}/collection-id-only/",
        {{model_name}}CollectionIdOnlyConsumer.as_asgi(),
    ),    
    path("channels/{{model_name|lower}}/record/view/<object_pk>/", {{model_name}}Consumer.as_asgi(), ),
]
"""

ASYNC_URLS_INIT_TEMPLATE = """ """

REST_URLS_INIT_TEMPLATE = """ """

REST_URLS_TEMPLATE = """
\"\"\"
Copyright (c) 2023, Lauro Cesar <lauro@hostcert.com.br>
All rights reserved under BSD 3-Clause License.
\"\"\"

from django.urls import path,include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter
from {{app_name|lower}}.views import {{model_name}}ViewSet,Serial{{model_name}}ViewSet, {{model_name}}IdOnlyViewSet
from django.conf import settings

router = DefaultRouter()

router.register(r'{{model_name|lower}}', {{model_name}}ViewSet,basename="{{model_name|lower}}")
router.register(r'serial-{{model_name|lower}}', Serial{{model_name}}ViewSet,basename="serial-{{model_name|lower}}")
router.register(r'{{model_name|lower}}-collection-id-only', {{model_name}}IdOnlyViewSet,basename="id-only-{{model_name|lower}}")

urlpatterns = [
	path('', include(router.urls))
]
"""

WEB_URLS_TEMPLATE = """
\"\"\"
Copyright (c) 2023, Lauro Cesar <lauro@hostcert.com.br>
All rights reserved under BSD 3-Clause License.
\"\"\"

from django.urls import path,include, re_path
from {{app_name|lower}}.views import {{model_name}}TemplateView,{{model_name}}DetailView, {{model_name}}ListView, {{model_name}}UpdateView, {{model_name}}DeleteView, {{model_name}}CreateView

urlpatterns = [    
    path("", {{model_name}}TemplateView.as_view(), name="{{model_name|lower}}-index"),    
    path("collection/", {{model_name}}ListView.as_view(), name="{{model_name|lower}}-list"),
    path("collection/<int:pk>/", {{model_name}}DetailView.as_view(), name='{{model_name|lower}}-detail'),
    path("collection/<int:pk>/editar/", {{model_name}}UpdateView.as_view(), name='{{model_name|lower}}-update'),
    path("collection/<int:pk>/remover/", {{model_name}}DeleteView.as_view(), name='{{model_name|lower}}-delete'),    
    path("collection/adicionar/", {{model_name}}CreateView.as_view(), name='{{model_name|lower}}-create'),
]
"""

WEB_URLS_INIT_TEMPLATE = """ """

CHANNELS_TEMPLATE = """
\"\"\"
Copyright (c) 2023, Lauro Cesar <lauro@hostcert.com.br>
All rights reserved under BSD 3-Clause License.
\"\"\"
import logging
logger = logging.getLogger(__name__)
import hashlib
import json
from project.celery_tasks import app
from asgiref.sync import sync_to_async
from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer,AsyncJsonWebsocketConsumer
from {{app_name}}.models import {{model_name}}

class {{model_name}}CollectionIdOnlyConsumer(AsyncJsonWebsocketConsumer):  
    @property
    def nome_do_grupo(self):
        return f"{{app_name}}_collection_id_only_{{model_name|lower}}"

    @property
    def groupID(self):
        return hashlib.md5(self.nome_do_grupo.encode("utf-8")).hexdigest()

    def can_view(self):
        self.user = self.scope["user"]        
        return True

    async def connect(self):
        self.user = self.scope["user"]        
        if self.user.is_authenticated:
            can_view = await sync_to_async(self.can_view)()
            if can_view:                             
                await self.channel_layer.group_add(self.nome_do_grupo, self.channel_name)        
                await self.accept()
        else:
            await self.close()


    async def disconnect(self, close_code):       
        pass

    async def receive_json(self, content):     
        await self.channel_layer.group_send(
            self.nome_do_grupo, {"type": "group_message", "content": content}
        )

    async def group_message(self, event):                    
        message = event["content"]
        await self.send_json(message)

    async def receive(self, text_data):
        await self.send(text_data=text_data)
        

class {{model_name}}CollectionConsumer(AsyncJsonWebsocketConsumer):   
    
    @property
    def nome_do_grupo(self):
        return f"{{app_name}}_collection_{{model_name|lower}}"

    @property
    def groupID(self):
        return hashlib.md5(self.nome_do_grupo.encode("utf-8")).hexdigest()

    def can_view(self):
        return True

    async def connect(self):
        self.user = self.scope["user"]        
        if self.user.is_authenticated:
            can_view = await sync_to_async(self.can_view)()
            if can_view:                             
                await self.channel_layer.group_add(self.nome_do_grupo, self.channel_name)        
                await self.accept()
        else:
            await self.close()


    async def disconnect(self, close_code):       
        pass

    async def receive_json(self, content):     
        await self.channel_layer.group_send(
            self.nome_do_grupo, {"type": "group_message", "content": content}
        )

    async def group_message(self, event):                    
        message = event["content"]
        await self.send_json(message)

    async def receive(self, text_data):
        await self.send(text_data=text_data)



class {{model_name}}Consumer(AsyncJsonWebsocketConsumer):
    object_pk =-1
    
    @property
    def nome_do_grupo(self):
        return f"{{model_name}}_{self.object_pk}" 

    @property
    def groupID(self):
        return hashlib.md5(self.nome_do_grupo.encode("utf-8")).hexdigest()
 
    def can_view(self):
        checklist = []
        try:
            logger.info(f"Check if user can connect to socket, object_pk= {self.object_pk}")           
            user = self.scope["user"]
            checklist = []
            if hasattr(user, "is_superuser"):
                checklist.append(user.is_superuser)
            if hasattr(user, "is_operator"):
                checklist.append(user.is_operator)
            records = {{model_name}}.objects.filter(pk=self.object_pk, criado_por=user)
            checklist.append(records.count()>0)
        except Exception as e:
            logger.error(e.__repr__())

        return True in checklist

    async def connect(self):
        self.user = self.scope["user"]        
        if self.user.is_authenticated:
            url_route = self.scope.get("url_route",{})
            route_kwargs = url_route.get("kwargs",{})
            self.object_pk =route_kwargs.get("object_pk","-1")
            can_view = await sync_to_async(self.can_view)()
            
            if can_view:                
                await self.channel_layer.group_add(self.nome_do_grupo, self.channel_name)        
                await self.accept()                
        else:
            await self.close()


    async def disconnect(self, close_code):       
        pass

    async def receive_json(self, content):     
        await self.channel_layer.group_send(
            self.nome_do_grupo, {"type": "group_message", "content": content}
        )

    async def group_message(self, event):                    
        message = event["content"]
        await self.send_json(message)

    async def receive(self, text_data):
        await self.send(text_data=text_data)

"""

CHANNELS_INIT_TEMPLATE = """\nfrom .{{save_to}} import {{model_name}}Consumer,{{model_name}}CollectionConsumer, {{model_name}}CollectionIdOnlyConsumer\n"""

SERIALIZER_INIT_TEMPLATE = """\nfrom .{{save_to}} import {{model_name}}Serializer,{{model_name}}IdOnlySerializer, {{model_name}}IdOnlySerializer,  Serial{{model_name}}Serializer\n"""

SERIALIZER_TEMPLATE = """
\"\"\"
Copyright (c) 2023, Lauro Cesar <lauro@hostcert.com.br>
All rights reserved under BSD 3-Clause License.
\"\"\"
from rest_framework import serializers
from {{app_name}}.models import {{model_name}}
from project.base_serializers import BaseSerializer


class {{model_name}}IdOnlySerializer(BaseSerializer):
    class Meta:
        model = {{model_name}}
        fields = ['id']
        if {{model_name}}.READ_ONLY_FIELDS:
            read_only_fields ={{model_name}}.READ_ONLY_FIELDS
            

class {{model_name}}Serializer(BaseSerializer):
    class Meta:
        model = {{model_name}}
        fields = {{model_name}}.SERIALIZABLES
        if {{model_name}}.READ_ONLY_FIELDS:
            read_only_fields ={{model_name}}.READ_ONLY_FIELDS

class Serial{{model_name}}Serializer(BaseSerializer):
    class Meta:
        model = {{model_name}}
        fields = ["serial"]
        if {{model_name}}.READ_ONLY_FIELDS:
            read_only_fields ={{model_name}}.READ_ONLY_FIELDS
            
"""

VIEW_INIT_TEMPLATE = """
from .{{save_to}} import (
    {{model_name}}TemplateView,
    {{model_name}}DetailView, 
    {{model_name}}ListView, 
    {{model_name}}UpdateView, 
    {{model_name}}CreateView, 
    {{model_name}}DeleteView,
    Serial{{model_name}}ViewSet,
    {{model_name}}IdOnlyViewSet,    
    {{model_name}}ViewSet)
"""

VIEW_TEMPLATE = """
\"\"\"
Copyright (c) 2023, Lauro Cesar <lauro@hostcert.com.br>
All rights reserved under BSD 3-Clause License.
\"\"\"
from rest_framework import viewsets
from rest_framework.parsers import JSONParser
from rest_framework.authentication import SessionAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from project.authentication import APITokenAuthentication
from django.views.generic import View
from django.http import JsonResponse
from django.middleware import csrf
from django.db import IntegrityError
from django.core.exceptions import ValidationError
import json
import re
from django.urls import reverse_lazy
from django.core.cache import cache
from django.utils.safestring import mark_safe
from project.celery_tasks import app
from django.contrib import messages
from django.views.generic.base import TemplateView
from django.http import JsonResponse
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.sites.shortcuts import get_current_site
from project.views import BaseTemplateView
from {{app_name}}.serializers import {{model_name}}Serializer, {{model_name}}IdOnlySerializer, Serial{{model_name}}Serializer
from {{app_name}}.models import {{model_name}}
from project.views import CustomBaseListView, CustomBaseDetailView, CustomBaseUpdateView, CustomBaseCreateView, CustomBaseDeleteView
from project.viewsets import BaseViewSetModel

class {{model_name}}DeleteView(CustomBaseDeleteView):
    template_name = "{{model_name|lower}}/web_templates/{{app_version}}/{{model_name|lower}}_delete.html"
    model = {{model_name}}
    success_url = reverse_lazy('{{model_name|lower}}-list')

class {{model_name}}CreateView(CustomBaseCreateView):
    template_name = "{{model_name|lower}}/web_templates/{{app_version}}/{{model_name|lower}}_create.html"
    model = {{model_name}}
    fields = {{model_name}}.CREATE_FIELDS
    success_url = reverse_lazy('{{model_name|lower}}-list')
 

class {{model_name}}UpdateView(CustomBaseUpdateView):
    template_name = "{{model_name|lower}}/web_templates/{{app_version}}/{{model_name|lower}}_update.html"
    model = {{model_name}}
    fields = {{model_name}}.CREATE_FIELDS
 

class {{model_name}}DetailView(CustomBaseDetailView):
    template_name = "{{model_name|lower}}/web_templates/{{app_version}}/{{model_name|lower}}_detail.html"
    model = {{model_name}}
 

class {{model_name}}ListView(CustomBaseListView):
    template_name = "{{model_name|lower}}/web_templates/{{app_version}}/{{model_name|lower}}_list.html"
    model = {{model_name}}
    paginate_by = 15
    allow_empty = True
    
class {{model_name}}TemplateView(BaseTemplateView):
    template_name = "{{model_name|lower}}/web_templates/{{app_version}}/{{model_name|lower}}_base.html"


class {{model_name}}ViewSet(BaseViewSetModel):
   serializer_class = {{model_name}}Serializer

class Serial{{model_name}}ViewSet(BaseViewSetModel):
   serializer_class = Serial{{model_name}}Serializer

class {{model_name}}IdOnlyViewSet(BaseViewSetModel):
   serializer_class = {{model_name}}IdOnlySerializer
   
"""

TASK_INIT_TEMPLATE = """\nfrom . import {{save_to}}\n"""

TASK_TEMPLATE = """
\"\"\"
Copyright (c) 2023, Lauro Cesar <lauro@hostcert.com.br>
All rights reserved under BSD 3-Clause License.
\"\"\"

import logging
logger = logging.getLogger(__name__)
from celery import shared_task
from django.conf import settings
from django.utils.encoding import smart_str
from PIL import Image, ImageOps, ImageDraw,ImageFont
from io import BytesIO
from django.core.cache import cache
from django.utils.text import slugify
import json
from django.urls import reverse_lazy
import base64
from project.celery_tasks import app
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from {{app_name}}.models import {{model_name}}
from {{app_name}}.serializers import {{model_name}}Serializer, {{model_name}}IdOnlySerializer


@shared_task(name="{{app_name}}_collection_id_only_{{model_name.lower()}}", max_retries=2, soft_time_limit=45)
def on_{{app_name}}_collection_id_only_{{model_name.lower()}}_task(object_pk):
    logger.debug(f"sending live update {object_pk}")
    instance = {{model_name}}.get_or_none(pk=object_pk)
    if instance:
        channel_layer = get_channel_layer()        
        try:                        
            serializador = {{model_name}}IdOnlySerializer(instance)
            async_to_sync(channel_layer.group_send)(
               f"{{app_name}}_collection_id_only_{{model_name|lower}}", {"type": "group_message", "content": serializador.data}
            )
        except Exception as e:           
            logger.error(e.__repr__())           
    else:
        logger.debug(f"Nao achei {object_pk}")
        
        
@shared_task(name="{{app_name}}_collection_{{model_name.lower()}}", max_retries=2, soft_time_limit=45)
def on_{{app_name}}_collection_id_only_{{model_name.lower()}}_task(object_pk):
    logger.debug(f"sending live update {object_pk}")
    instance = {{model_name}}.get_or_none(pk=object_pk)
    if instance:
        channel_layer = get_channel_layer()        
        try:                        
            serializador = {{model_name}}Serializer(instance)
            async_to_sync(channel_layer.group_send)(
               f"{{app_name}}_collection_{{model_name|lower}}", {"type": "group_message", "content": serializador.data}
            )
        except Exception as e:           
            logger.error(e.__repr__())           
    else:
        logger.debug(f"Nao achei {object_pk}")



@shared_task(name="stream_live_update_{{model_name.lower()}}", max_retries=2, soft_time_limit=45)
def on_stream_live_update_{{model_name.lower()}}_task(object_pk):
    instance = {{model_name}}.get_or_none(pk=object_pk)
    if instance:
        channel_layer = get_channel_layer()        
        try:                        
            serializador = {{model_name}}Serializer(instance)
            async_to_sync(channel_layer.group_send)(
                f"{{model_name}}_{object_pk}", {"type": "group_message", "content": serializador.data}
            )
        except Exception as e:           
            logger.error(e.__repr__())  
"""

SIGNAL_INIT_TEMPLATE = (
    """\nfrom .{{save_to}}  import  PostSave{{model_name}}Signals\n"""
)

SIGNAL_TEMPLATE = """
\"\"\"
Copyright (c) 2023, Lauro Cesar <lauro@hostcert.com.br>
All rights reserved under BSD 3-Clause License.
\"\"\"

from django.db.models.signals import (
    pre_save,
    post_save,
    pre_init,
    post_init,
    pre_delete,
    post_delete,
    m2m_changed,
)

import hashlib
from django.dispatch import receiver
from django.conf import settings
from project.celery_tasks import app
from {{app_name}}.models import {{model_name}}


@receiver(post_save, sender={{model_name}})
def PostSave{{model_name}}Signals(
    sender, instance, created, using, update_fields, *args, **kwargs
):
    if True in [created]:
        for task in {{model_name}}.TASKS.get('on_create',[]):
            app.send_task(task, [instance.id])
    else:
        for task in {{model_name}}.TASKS.get('on_save',[]):
            app.send_task(task, [instance.id])
"""

MODEL_INIT_TEMPLATE = """\nfrom .{{save_to}} import {{model_name}}\n"""

MODEL_TEMPLATE = """\"\"\"
Copyright (c) 2023, Lauro Cesar <lauro@hostcert.com.br>
All rights reserved under BSD 3-Clause License.
\"\"\"

import logging
logger = logging.getLogger(__name__)
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.encoding import smart_str
from django.conf import settings
import base64
from django.urls import reverse
from django.core.cache import cache
from django.utils.safestring import mark_safe
from project.celery_tasks import app
from django.contrib import messages
from project.models import BaseModel, StackedModel


class {{model_name}}(BaseModel):
    MODEL_LIST_ORDER_VALUE = 0
    SERIALIZABLES =['id','label','serial']
    FLUTTER_TYPES = {
        "default": "String",
        "id": "int",
    }
    FLUTTER_MANY_TO_MANY = {}
    FLUTTER_ONE_TO_ONE = {}    
    READ_ONLY_FIELDS=['id','serial']
    ADMIN_LIST_EDITABLE=[]
    ADMIN_LIST_DISPLAY=['label','rest_endpoint']
    ADMIN_ORDERING=[]
    ADMIN_FILTER_HORIZONTAL= []
    ADMIN_LIST_FILTER=[]
    ADMIN_SEARCH_FILTER=[]
    ADMIN_DISPLAY_LINKS=[]
    EXCLUDE_FROM_ADMIN=[]
    CREATE_FIELDS=[]
    FORM_FIELDS=[]
    REST_BASENAME="{{model_name.lower()}}"
 
    TASKS={
        'on_create':["{{app_name}}_collection_id_only_{{model_name.lower()}}","{{app_name}}_collection_{{model_name.lower()}}"],
        'on_save':["stream_live_update_{{model_name.lower()}}","{{app_name}}_collection_id_only_{{model_name.lower()}}","{{app_name}}_collection_{{model_name.lower()}}"],
        'on_delete':[]
    }

    @property
    def label(self):
        return "{{verbose_name}}"

    class Meta(BaseModel.Meta):
        verbose_name = _("{{verbose_name}}")
        verbose_name_plural = _("{{verbose_name_plural}}")

    def __str__(self):
        return self.label

"""


FLUTTER_MODEL_FORM_TEMPLATE = """



"""

FLUTTER_MODEL_TEMPLATE = """
import 'dart:convert';
import 'package:flutter/foundation.dart';
import 'package:built_collection/built_collection.dart';
import 'package:built_value/built_value.dart';
import 'package:built_value/serializer.dart';
import '/serializer.dart';

part '{{modelFileName}}.g.dart';

abstract class {{modelName}} implements Built<{{modelName}}, {{modelName}}Builder> {
	
	{{modelFields}}

	String toStandartJson() {
		return json.encode(standardSerializers.serializeWith({{modelName}}.serializer, this));
	}

	String toJson() {
		return json.encode(serializers.serializeWith({{modelName}}.serializer, this));
	}


	static {{modelName}} defaultModel() {
    	return {{modelName}}((s) {
			s
			{{defaultModelValues}};
    	});
  	}



  	static Future<{{modelName}}> fromStandartJsonAsync(String fromJson) async {
		  return await compute(fromStandartJson, fromJson);
  	}

	static {{modelName}} fromStandartJson(String fromJson) {
		try {
      		return standardSerializers.deserializeWith({{modelName}}.serializer, json.decode(fromJson)) ?? defaultModel();
    	} catch (error) {
      		return defaultModel();
    	}       
	}

	static {{modelName}} fromJson(String fromJson) {
		return serializers.deserializeWith(
				{{modelName}}.serializer, json.decode(fromJson)) ?? {{modelName}}();
	}
	

	static Serializer<{{modelName}}> get serializer => _${{builderName}}Serializer;

	{{modelName}}._();

	factory {{modelName}}([void Function({{modelName}}Builder ) updates]) = _${{modelName}};
}
"""

FLUTTER_COLLECTION_TEMPLATE = """

import 'dart:convert';
import 'package:flutter/foundation.dart';
import 'package:built_collection/built_collection.dart';
import 'package:built_value/built_value.dart';
import 'package:built_value/serializer.dart';
import '/serializer.dart';
{{collectionImports}}
part '{{modelFileName}}.g.dart';

abstract class {{collectionName}} implements Built<{{collectionName}}, {{collectionName}}Builder> {
	int get page;
	int get totalResults;
	int get totalPages;
	
	{{collectionModels}}

	String toStandartJson() {
		return json.encode(standardSerializers.serializeWith({{collectionName}}.serializer, this));
	}

	String toJson() {
		return json.encode(serializers.serializeWith({{collectionName}}.serializer, this));
	}


	static {{collectionName}} defaultModel() {
    	return {{collectionName}}((s) {
			s			
			..page = 1
			..totalPages = 0
			..totalResults = 0;
    	});
  	}

  	static Future<{{collectionName}}> fromStandartJsonAsync(String fromJson) async {
		  return await compute(fromStandartJson, fromJson);
  	}

	static {{collectionName}} fromStandartJson(String fromJson) {
		try {
      		return standardSerializers.deserializeWith({{collectionName}}.serializer, json.decode(fromJson)) ?? defaultModel();
    	} catch (error) {
      		return defaultModel();
    	}       
	}

	static {{collectionName}} fromJson(String fromJson) {
		return serializers.deserializeWith(
				{{collectionName}}.serializer, json.decode(fromJson)) ?? {{collectionName}}();
	}
	

	static Serializer<{{collectionName}}> get serializer => _${{builderName}}Serializer;

	{{collectionName}}._();

	factory {{collectionName}}([void Function({{collectionName}}Builder ) updates]) = _${{collectionName}};
}
"""


FLUTTER_COLLECTION_STATE_PROVIDER_TEMPLATE = """

/// {{wall_dir}}
/// {{model_dir}}
/// {{base_dir}}
/// {{app_path}}
/// {{app_name.title()}}
/// asyncAutomatic = false
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '/src/states/{{wall_dir}}/{{collection_state_dart_file}}';
import '/src/auth_wall/auth_state.dart';
import '/src/boot_wall/boot_state.dart';
import '/src/utils/app_constants.dart';

class {{modelName}}CollectionProvider extends StatelessWidget {
  final Widget childWidget;

  const {{modelName}}CollectionProvider({Key? key, required this.childWidget}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MultiProvider(providers: [
      ChangeNotifierProvider(
          create: (_) => {{modelName}}CollectionState(classProperties: {
            "authHeaders": context.read<AuthState>().authHeaders,
            "ssoToken": context.read<AuthState>().authToken,
            "asyncAutomatic":false,
            "createRestEndPoint":"${AppConstants.restBaseUrl}/{{modelName.lower()}}/",
            "restEndPoint":"${AppConstants.restBaseUrl}/{{modelName.lower()}}-collection-id-only/",
            "socketEndPoint":"${AppConstants.baseWsUrl}/channels/{{modelName.lower()}}/collection-id-only/",            
            "keyName":
            "_{{modelName.lower()}}_collection_${context.read<AuthState>().accountID}_${context.read<BootState>().packageInfo
                .buildNumber}"
          })
            ..onInit()),
    ], child: childWidget);
  }
}


"""

FLUTTER_MODEL_STATE_PROVIDER_TEMPLATE = """
/// {{wall_dir}}
/// {{model_dir}}
/// asyncAutomatic = false
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '/src/states/{{wall_dir}}/{{model_state_dart_file}}';
import '/src/auth_wall/auth_state.dart';
import '/src/boot_wall/boot_state.dart';
import '/src/utils/app_constants.dart';

class {{modelName}}RecordProvider extends StatelessWidget {
  final Widget childWidget;
  final int recordId;

  const {{modelName}}RecordProvider({Key? key, required this.childWidget, required this.recordId}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MultiProvider(providers: [
      ChangeNotifierProvider(
          create: (_) => {{modelName}}RecordState(classProperties: {
            "authHeaders": context.read<AuthState>().authHeaders,
            "ssoToken": context.read<AuthState>().authToken,
            "asyncAutomatic":false,
            "restEndPoint": "${AppConstants.restBaseUrl}/{{modelName.lower()}}/$recordId.json",
            "serialRestEndPoint": "${AppConstants.restBaseUrl}/serial-{{modelName.lower()}}/$recordId.json",
            "socketEndPoint": "${AppConstants.baseWsUrl}/channels/{{modelName.lower()}}/record/view/$recordId/",
            "keyName":
            "_{{modelName.lower()}}_${context.read<AuthState>().accountID}_${recordId}_${context.read<BootState>().packageInfo
                .buildNumber}"
          })
            ..onInit()),
    ], child: childWidget);
  }
}

"""

FLUTTER_COLLECTION_STATE_TEMPLATE = """
import '/src/utils/app_notifier/app_collection_rest_notifier.dart';

class {{modelName}}CollectionState extends AppCollectionRestAndSocketNotifier {
  {{modelName}}CollectionState({required super.classProperties});

  @override
  bool get isReady => activePage >0;

}

"""

FLUTTER_MODEL_STATE_TEMPLATE = """
import '/src/utils/app_notifier/app_record_rest_notifier.dart';

class {{modelName}}RecordState extends AppRecordRestAndSocketNotifier {
  {{modelName}}RecordState({required super.classProperties});

  @override
  bool get isReady => record.containsKey("id");
  
  {{flutter_model_state_fields}}

}

"""

ADMIN_INIT_TEMPLATE = """\nfrom .{{save_to}} import {{model_name}}Admin\n"""

ADMIN_TEMPLATE = """
\"\"\"
Copyright (c) 2023, Lauro Cesar <lauro@hostcert.com.br>
All rights reserved under BSD 3-Clause License.
\"\"\"
from django.contrib import admin
from django.core.cache import cache
from django.utils.safestring import mark_safe
from project.celery_tasks import app
from django.contrib import messages
import base64
from django.utils.translation import gettext_lazy as _
from project.admin import ProjectBaseModelAdmin as BaseModelAdmin
from {{app_name}}.models import {{model_name}}
from project.admin import dashboard_sites, admin_sites
import numpy as np

class {{model_name}}Admin(BaseModelAdmin):
    save_on_top = True
    ordering = {{model_name}}.ADMIN_ORDERING
    list_display = {{model_name}}.ADMIN_LIST_DISPLAY
    list_filter = {{model_name}}.ADMIN_LIST_FILTER
    search_fields = {{model_name}}.ADMIN_SEARCH_FILTER
    list_editable = {{model_name}}.ADMIN_LIST_EDITABLE
    list_display_links={{model_name}}.ADMIN_DISPLAY_LINKS
    filter_horizontal= {{model_name}}.ADMIN_FILTER_HORIZONTAL    
    exclude = list(np.unique([item for sublist in [BaseModelAdmin.exclude,{{model_name}}.EXCLUDE_FROM_ADMIN] for item in sublist]))
    

    def has_delete_permission(self, request, obj=None):
        user = request.user
        checklist = []
        if hasattr(user, "is_rootuser"):
            checklist.append(user.is_rootuser)
        if hasattr(user, "is_superuser"):
            checklist.append(user.is_superuser)
        if hasattr(user, "is_operator"):
            checklist.append(user.is_operator)    
        
        if obj is not None:
            checklist.append(obj.criado_por in [user]) 
        return (True in checklist)


for admin_site in admin_sites:
    admin_site.register({{model_name}},{{model_name}}Admin)


for developer_site in dashboard_sites:
    developer_site.register({{model_name}},{{model_name}}Admin)

"""
