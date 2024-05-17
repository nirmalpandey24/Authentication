from django.http import JsonResponse
from django.views import View
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt  
from django.contrib.auth.hashers import make_password
from .models import CustomUser
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
import json
import jwt ,datetime
class CustomUserInfo(View):
    @csrf_exempt  
    def dispatch(self, *args, **kwargs):  #called before method handlder (get,post) ,kun method vanera detemine
        return super().dispatch(*args, **kwargs)

    def get(self, request,id):
        users = list(CustomUser.objects.filter(pk=id).values())
        # users_data = [{
        #     'id':user.id,
        #     'email': user.email,
        #     'eid': user.eid,
        #     'ename': user.ename,
        #     'esalary': user.esalary,
        #     'username': user.username,
        #     'phone_number': user.phone_number,
        #     'address': user.address,
        #     'gender': user.gender,
        #     'hobbies': user.hobbies,
        #     'isDeleted': user.isDeleted
        # } for user in users]
        # # print(users_data)
        return JsonResponse(users, status=200, safe=False)  # Set safe=False here

    def put(self, request, id):
        user = get_object_or_404(CustomUser, id=id)
        data = json.loads(request.body)
        user.email = data.get('email', user.email)
        user.eid = data.get('eid', user.eid)
        user.ename = data.get('ename', user.ename)
        user.esalary = data.get('esalary', user.esalary)
        user.username = data.get('username', user.username)
        user.phone_number = data.get('phone_number', user.phone_number)
        user.address = data.get('address', user.address)
        user.gender = data.get('gender', user.gender)
        user.hobbies = data.get('hobbies', user.hobbies)
        user.save()
        return JsonResponse({'message': 'User updated'}, status=200)

    def patch(self, request, id):
        user = get_object_or_404(CustomUser, id=id)
        data = json.loads(request.body)
        for field, value in data.items(): #key-value pair iterate
            setattr(user, field, value)
        user.save()
        return JsonResponse({'message': 'User updated'}, status=200)

    def delete(self, request, id):
        user = get_object_or_404(CustomUser, id=id)              
        user.isDeleted = True
        user.save()
        return JsonResponse({"msg": "User deleted"}, status=204)


class CustomUserDetail(View):
    @csrf_exempt  
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        users = CustomUser.objects.all()
        users_data = [{
            'id':user.id,
            'email': user.email,                  #dis kvp
            'eid': user.eid
,
            'ename': user.ename,
            'esalary': user.esalary,
            'username': user.username,
            'phone_number': user.phone_number,
            'address': user.address,
            'gender': user.gender,
            'hobbies': user.hobbies,
            'isDeleted': user.isDeleted
        } for user in users]
        return JsonResponse(users_data, status=200,safe=False)

    def post(self, request):
        data = json.loads(request.body)
        user = CustomUser.objects.create(
            password = make_password(data.get('password')),  #save garni vanda agadi hash garni
            email=data.get('email'),
            eid=data.get('eid'),
            ename=data.get('ename'),
            esalary=data.get('esalary'),
            username=data.get('username'),
            phone_number=data.get('phone_number'),
            address=data.get('address'),
            gender=data.get('gender'),
            hobbies=data.get('hobbies')
        )
        return JsonResponse({'message': 'User created'}, status=201)

class LoginView(View):
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        password = data['password']

        user = CustomUser.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed("User not found!")

        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect password")

        access_token_payload = {
            'id': user.id,
            'exp': datetime.datetime.now() + datetime.timedelta(minutes=1),  
            'iat': datetime.datetime.now(),
            'user': user.email
        }
        access_token = jwt.encode(access_token_payload, 'secret', algorithm='HS384')

       
        refresh_token_payload = {
            'id': user.id,
            'exp': datetime.datetime.now() + datetime.timedelta(days=15), 
            'iat': datetime.datetime.now(),
        }
        refresh_token = jwt.encode(refresh_token_payload, 'refresh_secret', algorithm='HS384')

        
        response = JsonResponse({'token': access_token, 'refresh_token': refresh_token})
        response.set_cookie(key='jwt', value=access_token, httponly=True,samesite=None)
        response.set_cookie(key='refresh_token', value=refresh_token, httponly=True,samesite=None)

        return response
    

class UserView(View):
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def post(self,request):
        data = json.loads(request.body)
        email = data['email']
        password = data['password']

        user = CustomUser.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed("User not found!")

        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect password")
        access_token=request.COOKIES.get('jwt')
        refresh_token= request.COOKIES.get('refresh_token')
        time=datetime.datetime.now()
        new=int(time.timestamp())
        if not access_token:
            raise AuthenticationFailed('Unauthenticated')
        try:
            access_token_payload=jwt.decode(access_token,'secret',algorithms='HS384')
            

        except jwt.ExpiredSignatureError:
            refresh_token_payload=jwt.decode(refresh_token,'refresh_secret',algorithms='HS384')
            if new<refresh_token_payload['exp']:
                 access_token_payload = {
                    'id': user.id,
                    'exp': datetime.datetime.now() + datetime.timedelta(minutes=1),  
                    'iat': datetime.datetime.now(),
                    'user': user.email
                }
                 access_token = jwt.encode(access_token_payload, 'secret', algorithm='HS384')
                 response = JsonResponse({'token': access_token, })
                 response.set_cookie(key='jwt', value=access_token, httponly=True)
                 return response
            raise AuthenticationFailed('Unauthenticated')

        return JsonResponse(access_token_payload,safe=False)

