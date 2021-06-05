from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Connection, ChatMessage

# Create your views here.

@csrf_exempt
def test(request):
    print(request.body)
    return JsonResponse({"message":"Hello Daud"}, status=200)


def _parse_body(body):
   body_unicode = body.decode('utf-8')
   return  json.loads(body_unicode)

# print(_parse_body(body="hello"))

@csrf_exempt
def connect(request):
    body = _parse_body(json.loads(request.body))
    # print(request.body)
    print(body)
    connection_id = body['connectionId']
    new_connection = Connection.objects.get(connection_id=connection_id)
    new_connection.save()
    print(connection_id)
    return JsonResponse("connect successfully", status=200)


@csrf_exempt
def disconnect(request):
    body = _parse_body(request.body)
    connection_id = body['connectionId']
    new_connection = Connection.objects.get(connection_id=connection_id)
    new_connection.delete()
    return JsonResponse("disconnect successfully", status=200)