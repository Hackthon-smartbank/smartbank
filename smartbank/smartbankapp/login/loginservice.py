from rest_framework.authentication import TokenAuthentication

from smartbankapp.models import *
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate
import json
from rest_framework.authtoken.models import Token


@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([TokenAuthentication])
def create_new_user(request):
    body_data = json.loads(request.body)
    username = body_data.get('username')
    password = body_data.get('password')
    role = body_data.get('role')
    if not username or not password or not role:
        return HttpResponse(json.dumps({"Error":"Username or password or role cannot be empty"}),content_type='application/json')
    if User.objects.filter(username=username).exists():
        return HttpResponse(json.dumps({"Error":"User already exists"}),content_type='application/json')

    if role in ('admin','Admin'):
        role=1
    else:
        role=2 #customer
    user = User.objects.create_user(username=username, password=password,role=role)
    token,_ = Token.objects.get_or_create(user=user)
    return HttpResponse(json.dumps({"success":"successfully Created","User":user.username,"token":token.key}),content_type='application/json')

@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([TokenAuthentication])
def login_get_token(request):
    body_data = json.loads(request.body)
    username = body_data.get('username')
    password = body_data.get('password')
    if not username or not password:
        return HttpResponse(json.dumps({"Error": "Username or password cannot be empty"}),
                            content_type='application/json')
    user = authenticate(username=username, password=password)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return HttpResponse(json.dumps({'message': 'Login successful', 'token': token.key}),
                            content_type='application/json')
    return HttpResponse(json.dumps({'error': 'Invalid credentials'}, status=400))




