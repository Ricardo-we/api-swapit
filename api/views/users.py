import random
from api.models import User, ConfirmationCode, UserContactInformation
from api.serializers import UserContactInfoSerializer, UserSerializer
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, parser_classes, permission_classes
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings
from api.utils.check_token_and_user import check_user_and_token

def validations(request, email_required=False):
    if not request.data.get('username'): raise ValueError('Username required for sign up')
    if not request.data.get('password'): raise ValueError('Password required for sign up')
    if email_required and not request.data.get('email'): raise ValueError('Email required for sign up')
    return True

def generate_confirmation_code():
    random_numbers = ''
    for i in range(4):
        random_numbers += str(random.randint(0, 9))
    return random_numbers

@api_view(['POST'])
@parser_classes([JSONParser])
@csrf_exempt
def create_user(request):
    try:
        validations(request, True)
        code = generate_confirmation_code()
        
        if User.objects.filter(username=request.data['username']).exists(): 
            raise Exception('Username already in use')
        if ConfirmationCode.objects.filter(username=request.data.get('username')).exists():
            ConfirmationCode.objects.filter(username=request.data.get('username')).first().delete()
        ConfirmationCode.objects.create(username=request.data.get('username'), code=code)

        send_mail(
            f'Welcome {request.data["username"]} to: app', 
            f'Please send the confirmation code {code}', 
            settings.EMAIL_HOST_USER, 
            [request.data.get('email')]
        )
        
        return Response({'message':'Confirm your email'})
    except Exception as error: 
        print(error)
        return Response({'error': str(error)})

@api_view(['POST'])
@parser_classes([JSONParser])
@csrf_exempt
def confirm_user_creation(request, confirmation_code):
    try:
        if not confirmation_code: raise Exception('Not a confirmation code')
        validations(request, True)

        confirmation_code_ = ConfirmationCode.objects.filter(
            username=request.data['username'], 
            code=confirmation_code
        ).first()
        if (not confirmation_code_):   
            raise Exception('Invalid code')
            
        user = User.objects.create_user(
            username=request.data['username'],
            email=request.data['email'],
            password=request.data['password'],
            location=request.data.get('location'),
            user_currency=request.data.get('user_currency')
        )
        token = Token.objects.create(user=user)
        confirmation_code_.delete()
        
        return Response({'user': UserSerializer(user).data , 'auth_token': token.key})
    except Exception as err:
        return Response({'error':str(err)})

@api_view(['POST'])
@parser_classes([JSONParser])
@csrf_exempt
def login(request):
    try:
        if not request.data.get('username'): raise ValueError('Username required for login')
        if not request.data.get('password'): raise ValueError('Password required for login')

        user = User.objects.get(username=request.data['username'])
        if not user or not user.check_password(request.data['password']): raise Exception('Invalid password') 

        Token.objects.filter(user=user).first().delete()        
        token = Token.objects.create(user=user)

        return Response({'auth_token': str(token.key), 'user': UserSerializer(user).data})
    except Exception as error:
        return Response({'error': str(error)})
    
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

def update_user(request, user: User):
    user.username = request.data.get('username') or user.username
    user.phone_number = request.data.get('phone_number') or user.phone_number
    user.location = request.data.get('location') or user.location
    user.user_currency = request.data.get('user_currency') or user.user_currency

    if request.data.get('password'): 
        user.set_password(request.data['password'])
    serializer = UserSerializer(user)
    return Response(serializer.data)

@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def users_detail(request, pk):
    try:
        check_user_and_token(pk, request.headers['Authorization'])
        user = User.objects.get(pk=pk)
        if request.method == 'GET':
            data = UserSerializer(user, many=False).data
            return Response(data)
        elif request.method == 'PUT':
            return update_user(request, user)
        elif request.method == 'DELETE':
            # user.delete()
            # return Response({'message': f'User with id: {user.id} is deleted'}, status=200)
            return Response({'message': 'User deletion desactivated'})
    except Exception as error:
        return Response({'error': str(error)})


# ADD-DELETE USER-CONTACT-INFO

