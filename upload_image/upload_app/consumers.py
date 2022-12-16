# topic routing

from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer
import time
from random import randint
import json
import mysql.connector
import mysql
import asyncio
from asgiref.sync import async_to_sync  # sync to async

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="employeedb",
)

mycursor = mydb.cursor()


class MySyncConsumer(SyncConsumer):

    def websocket_connect(self, event):
    
        print(self.channel_layer)
        print(self.channel_name)
        
        self.group_name=self.scope['url_route']['kwargs']['group_name_sc']

        async_to_sync(self.channel_layer.group_add)(
            self.group_name, self.channel_name)

        self.send({
            'type': 'websocket.accept'
        })

        print("group_name : ",self.group_name)
        print("websocket connected...", event)

    def websocket_receive(self, event):
        print('massage recived...')
        print('massage is : ', event['text'])

        self.send({
            'type': 'websocket.send',
            'text': 'message from server'
        })

        async_to_sync( self.channel_layer.group_send)(self.group_name,{
            'type':'chat.message',
            'message':event['text']
        })

    def chat_message(self,event):
        print("Event : ",event['message'])
        
        self.send({
            'type':'websocket.send',
            'text':event['message']
        })
       

    def websocket_disconnect(self, event):
        print('websocket disconnected...', event)
        print("discard : ",self.channel_layer)
        print("discard : ",self.channel_name)
        
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name, self.channel_name)

        raise StopConsumer()

class MyAsyncConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        print("ok")
        print(self.channel_layer)
        print(self.channel_name)

        await self.channel_layer.group_add(
            self.group_name, self.channel_name)

        await self.send({
            'type': 'websocket.accept'
        })

        print("websocket connected...", event)

    async def websocket_receive(self, event):
        print('massage recived...')
        print('massage is : ', event['text'])

        await self.send({
            'type': 'websocket.send',
            'text': 'message from server'
        })

        await self.channel_layer.group_send(self.group_name,{
            'type':'chat.message',
            'message':event['text']
        })

    async def chat_message(self,event):
        print("Event : ",event['message'])
        await self.send({
            'type':'websocket.send',
            'text':event['message']
        })
    
    async def websocket_disconnect(self, event):
        print('websocket disconnected...', event)
        print("disczrd : ",self.channel_layer)
        print("disczrd : ",self.channel_name)
        
        await self.channel_layer.group_discard(
            self.group_name, self.channel_name)

        raise StopConsumer()

 