from django.http import JsonResponse
from django.core.mail import send_mail
from django.contrib.auth.hashers import check_password
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from datetime import datetime, timedelta
import jwt
from backend.settings import (
    SECRET_KEY, 
    FERNET_ENCODE_KEY, 
    EMAIL_HOST_USER,
)
from backend.fernet import *
from backend.decorators import is_owner
from authc.serializers import UserSerializer
from authc.models import User
from car.models import Car


def jwt_verify_encode(username: str, email: str, password: str) -> str:
    dt = datetime.now() + timedelta(days=30)
    payload = {
        'email': str(email),
        'username': str(username),
        'password': str(password),
        'exp': dt
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm='HS256'
    )

    return token


def login(request): 
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            try:
                user = User.objects.get(email=serializer.data['email'])
                dt = datetime.now() + timedelta(days=60)
                if check_password(serializer.data['password'], user.password): 
                    res = JsonResponse('user succ logged', safe=False)
                    res.set_cookie(
                        key='utoken',
                        value=fernet_msg_encode(user.token),
                        expires=int(dt.strftime('%s')),
                    )
                    user.is_active = True
                    user.save()
                    return res

                else:
                    return JsonResponse('wrong data (email, password)', status=404, safe=False)

            except user.DoesNotExist:
                return JsonResponse('wrong data (email, password)', status=404, safe=False)

        return JsonResponse(serializer.errors, status=400)
        


def register_send_mail(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = UserSerializer(data=data)
        # check if user with this email/username already exist
        try:
            exist_email = User.objects.get(email=serializer.data['email'])
            exist_username = User.objects.get(username=serializer.data['username'])
            return JsonResponse('user already exist', status=400, safe=False)
        
        except exist_email.DoesNotExist or exist_username.DoesNotExist:
            if serializer.is_valid():
                token = jwt_verify_encode(
                    username=serializer.data['username'],
                    email=serializer.data['email'],
                    password=serializer.data['password']
                )

                try:
                    send_mail(
                        'email verification',
                        f'click to verify email http://127.0.0.1:8000/authc/verify/{token}',
                        EMAIL_HOST_USER,
                        [serializer.data['email']],
                    )
                    return JsonResponse('message was succ send', safe=False)
                
                except:
                    return JsonResponse('oops, an occured error', status=500, safe=False)
                
            return JsonResponse(serializer.errors, status=400)



def register_final_verify(request, token):
    if request.method == 'GET':
        try:
            decrypted_token = fernet_msg_decode(token)
            decoded_data = jwt.decode(decrypted_token, SECRET_KEY, algorithms=['HS256'])

            #check if user with this email/username already exist
            try:
                exist_email = User.objects.get(email='email')
                exist_username = User.objects.get(username='username')
                return JsonResponse('user already exist', status=400, safe=False)

            except exist_email.DoesNotExist or exist_username.DoesNotExist:
                new_user = User.objects.create_user(
                    username=decoded_data['username'],
                    email=decoded_data['email'],
                    password=decoded_data['password']
                )

                dt = datetime.now() + timedelta(days=60)
                res = JsonResponse('user succ created')
                res.set_cookie(
                    key='utoken',
                    value=fernet_msg_encode(new_user.token),
                    expires=int(dt.strftime('%s')),
                )

                new_user.is_active = True
                new_user.save()

                return res
        
        except jwt.ExpiredSignatureError:
            return JsonResponse('verify token timed out', status=400, safe=False)

        except:
            return JsonResponse('oops, an occured error', status=500, safe=False)
        

@csrf_exempt
@is_owner
def profile(request, upk):
    if request.method == 'GET':
        try:
            user = User.objects.get(pk=upk)
            cars = Car.objects.filter(car_pk=user.pk)
            if len(cars) > 0:
                titles = []
                for car in cars:
                    titles.append([car.company_name, car.model_name])
            else:
                titles = ''

            data = {
                'username': user.username,
                'email': user.email,
                'threads': titles,
            }
            return JsonResponse(data=data, safe=False)
        
        except user.DoesNotExist:
            return JsonResponse('user not found', status=404, safe=False)
