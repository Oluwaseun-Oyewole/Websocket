import re
from django.db import connection
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import boto3
from .models import Connection, ChatMessage
from django.contrib.auth.models import User

# Create your views here.

@csrf_exempt
def test(request):
    print("hello")
    print(request.body.decode("utf-8"))
    return JsonResponse({"message":"Hello Daud"}, status=200)

def _parse_body(body):
   body_unicode = body.decode('utf-8')
   return  json.loads(body_unicode)

@csrf_exempt
def connect(request):
    body = _parse_body(request.body)
    connection_id = body['connectionId']
    connections = Connection.objects.create(connection_id=connection_id)
    # print(connections)
    return JsonResponse("connect successfully", status=200, safe=False)


@csrf_exempt
def disconnect(request):
    body = _parse_body(request.body)
    connection_id = body['connectionId']
    connections = Connection.objects.get(connection_id=connection_id)
    connections = Connection.objects.all()
    # for connection in connections:
    #     connection.delete()
    return JsonResponse("disconnect successfully", status=200, safe=False)


# helper function
def _send_to_connection(connection_id, data):
    gatewayapi=boto3.client('apigatewaymanagementapi', endpoint_url="https://o4wgsdn9ga.execute-api.us-east-1.amazonaws.com/test",region_name="us-east-1", aws_access_key_id="AKIAWK22EWERS3O2HM4S",aws_secret_access_key="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", )
    response = gatewayapi.post_to_connection(ConnectionId=connection_id, Data=json.dumps(data).encode('utf-8'))
    return response


@csrf_exempt
def send_message(request):

    # for registered users    
    users = User.objects.all()
    confirm_username = []
    for user in users:
        confirm_username.append(user.username)
        
    body = _parse_body(request.body)
    dictionary_body = dict(body)
    username = dictionary_body['body']['username']
    timestamp = dictionary_body['body']['timestamp']
    content = dictionary_body['body']['content']
    
    if username in confirm_username:
         ChatMessage.objects.create(username=username, timestamp=timestamp, messages=content)
    else:
        print("Messages can only be sent by registered users")
        
    connections = Connection.objects.all()
    messages = {
        "username":username,
        "timestamp":timestamp,
        "messages":content
    }
    data = {"messages":[messages]} 
    
    for connection in connections:
        _send_to_connection(connection.connection_id, data)
    return JsonResponse({"message":"successfully sent"}, status=200, safe=False)

    

@csrf_exempt
def recent_messages(request):
    chat_messages = ChatMessage.objects.all()
    connections = Connection.objects.all()
    body = _parse_body(request.body)
    connection = body['connectionId']
    # connection_id = Connection.objects.get(connection_id=connection).connection_id
    recent_messages = []
    
    for chat_message in chat_messages:
        id = chat_message.id
        username = chat_message.username
        message = chat_message.messages
        timestamp = chat_message.timestamp
        
        messages = {
            "id":id,
            "username": username,
            "message": message,
            "timestamp": timestamp
        }
        recent_messages.append(messages)         
    data = {"message":recent_messages[::-1]}
    for connection in connections:
        _send_to_connection(connection.connection_id, data)
    return JsonResponse({"messages": "recent_messages"}, status=200)