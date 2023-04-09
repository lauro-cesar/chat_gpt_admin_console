
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
from channels.generic.websocket import AsyncWebsocketConsumer,AsyncJsonWebsocketConsumer
from chats.models import Answer

class AnswerCollectionIdOnlyConsumer(AsyncJsonWebsocketConsumer):  
    @property
    def nome_do_grupo(self):
        return f"chats_collection_id_only_answer"

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
        

class AnswerCollectionConsumer(AsyncJsonWebsocketConsumer):   
    
    @property
    def nome_do_grupo(self):
        return f"chats_collection_answer"

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



class AnswerConsumer(AsyncJsonWebsocketConsumer):
    object_pk =-1
    
    @property
    def nome_do_grupo(self):
        return f"Answer_{self.object_pk}" 

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
            records = Answer.objects.filter(pk=self.object_pk, criado_por=user)
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
