from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from .serializers import UserSigninSerializer
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_409_CONFLICT,
)
from rest_framework.response import Response
from rest_framework import viewsets
from .serializers import UserSigninSerializer, UsersSerializer
from .authentication import token_expire_handler, expires_in
from .models import User
import random as rand

from django.core.mail import send_mail
from django.conf import settings
import requests

def convert_timedelta(duration):
    """Converts a timedelta into hours, minutes, and seconds."""
    days, seconds = duration.days, duration.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 60)
    return hours, minutes, seconds

@api_view(["POST"])
@permission_classes([AllowAny])
def signin(request):
    signin_serializer = UserSigninSerializer(data=request.data)
    if not signin_serializer.is_valid():
        return Response(signin_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    email = signin_serializer.data['username']  # Usamos 'username' como el campo de correo electrónico
    password = signin_serializer.data['password']
    
    # Autenticamos al usuario
    user = authenticate(request=request, username=email, password=password)

    if not user:
        return Response({'detail': 'Invalid Credentials or activate account'}, status=status.HTTP_404_NOT_FOUND)

    # Generamos el token de acceso y refresh
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    refresh_token = str(refresh)

    return Response({
        'user_id': str(user.id),
        'name': str(user.name),
        'user_email': str(user.email),
        'accessToken': access_token,
        'refreshToken': refresh_token,
    })
@api_view(["POST"])
@permission_classes((AllowAny,))
def forgotPassword(request):
    emailR = request.data.get('email')
    try:
        user = User.objects.get(email=emailR)
    except User.DoesNotExist:
        return Response(status=HTTP_404_NOT_FOUND, data={"message": "Email not found!"})

    random_number = rand.randint(10000, 100000)
    user.verification_code = random_number
    user.change_pwd = True
    user.save()

    message = requests.post(
        "https://api.mailgun.net/v3/mg.zuntexapparel.com/messages",
        auth=("api", "883b9bbbf30e46e0a0cbc954f9b49e89-90ac0eb7-ab95c27b"),
        data={
            "from": "Zuntex Apparel <no-reply@zuntexapparel.com>",
            "to": emailR,
            "subject": "Your Fenix verification code",
            "text": "Your verification code is " + str(random_number)
        }
    )
    
    if message.status_code == 200:
        return Response(status = HTTP_200_OK, data={"message": "Email sent!"})
    else:
        return Response(status=HTTP_409_CONFLICT, data={"message": "There was an issue sending the email!"})

@api_view(["POST"])
@permission_classes((AllowAny,))
def confirmToken(request):
    email = request.data.get('email')
    token = request.data.get('token')

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response(status=HTTP_404_NOT_FOUND, data={"message": "Email not found!"})

    if user.verification_code == token:
        user.change_pwd = False
        user.save()
        return Response(status=HTTP_200_OK)
    else:
        return Response(status=HTTP_409_CONFLICT, data={"message": "Token does not match!"})

@api_view(["POST"])
@permission_classes((AllowAny,))
def resetPassword(request):
    email = request.data.get('user_identification')
    new_password = request.data.get('user_new_token')

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response(status=HTTP_404_NOT_FOUND, data={"message": "User not found!"})

    if user.change_pwd == False:
        user.set_password(new_password)
        try:
            user.save()
            return Response(status=HTTP_200_OK, data={"message": "Password changed!"})
        except Exception as e:
            return Response(status=HTTP_409_CONFLICT, data={"message": "Could not set the password!"})
    else:
        return Response(status=HTTP_409_CONFLICT, data={"message": "Invalid request!"})

class UsersModelViewSet(viewsets.ModelViewSet):
    """Handle creating and updating users."""
    serializer_class = UsersSerializer
    queryset = User.objects.all()  # Ensure this is appropriate for your version of Django (e.g., Django 5.1.4)
