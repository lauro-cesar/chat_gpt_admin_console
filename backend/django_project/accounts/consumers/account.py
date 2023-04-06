"""
Copyright (c) 2023, Lauro Cesar <lauro@hostcert.com.br>
All rights reserved under BSD 3-Clause License.
"""

import logging

logger = logging.getLogger(__name__)
import hashlib
import json
from project.celery_tasks import app
from asgiref.sync import sync_to_async
from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import (
    AsyncWebsocketConsumer,
    AsyncJsonWebsocketConsumer,
)
from accounts.models import Account


class AccountCollectionConsumer(AsyncJsonWebsocketConsumer):
    model_meta = Account._meta

    @property
    def nome_do_grupo(self):
        return f"accounts_collection_account"

    @property
    def groupID(self):
        return hashlib.md5(self.nome_do_grupo.encode("utf-8")).hexdigest()

    def can_view(self):
        self.user = self.scope["user"]
        if self.user.is_authenticated:
            return self.user.has_perm(
                f"{self.model_meta.app_label}.view_{self.model_meta.model_name}"
            )
        return False

    async def connect(self):
        self.user = self.scope["user"]
        if self.user.is_authenticated:
            can_view = await sync_to_async(self.can_view)()
            if can_view:
                await self.channel_layer.group_add(
                    self.nome_do_grupo, self.channel_name
                )
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


class AccountConsumer(AsyncJsonWebsocketConsumer):
    object_pk = -1
    model_meta = Account._meta

    @property
    def nome_do_grupo(self):
        return f"Account_{self.object_pk}"

    @property
    def groupID(self):
        return hashlib.md5(self.nome_do_grupo.encode("utf-8")).hexdigest()

    def can_view(self):
        self.user = self.scope["user"]
        if self.user.is_authenticated:
            return self.user.has_perm(
                f"{self.model_meta.app_label}.view_{self.model_meta.model_name}"
            )
        return False

    async def connect(self):
        self.user = self.scope["user"]
        if self.user.is_authenticated:
            can_view = await sync_to_async(self.can_view)()
            if can_view:
                url_route = self.scope.get("url_route", {})
                route_kwargs = url_route.get("kwargs", {})
                self.object_pk = route_kwargs.get("object_pk", "-1")
                await self.channel_layer.group_add(
                    self.nome_do_grupo, self.channel_name
                )
                await self.accept()
                app.send_task("stream_live_update_account", [self.object_pk])
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
