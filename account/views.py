from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import status
from .serializers import SignUpSerializer
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.utils import timezone  # Import Django's timezone utilities


@api_view(['POST'])
def register(request):
    data = request.data
    serializer = SignUpSerializer(data=data)
    if serializer.is_valid():
        if not User.objects.filter(username=data['email']).exists():
            user = User.objects.create(
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data['email'],
                username=data['email'],  # Using email as username
                password=make_password(data['password']),
            )
            return Response({'details': 'Your account registered successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'Error': 'This email already exists!'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_current_host(request):
    protocol = 'https' if request.is_secure() else 'http'
    host = request.get_host()
    return "{protocol}://{host}/".format(protocol=protocol, host=host)


@api_view(['POST'])
def forgot_password(request):
    try:
        data = request.data
        user = get_object_or_404(User, email=data['email'])
        
        token = get_random_string(40)
        expire_date = timezone.now() + timedelta(minutes=30)
        
        user.profile.reset_password_token = token
        user.profile.reset_password_expire = expire_date
        user.profile.save()

        host = get_current_host(request)
        link = "{protocol}://{host}/api/reset_password/{token}".format(protocol=request.scheme, host=host, token=token)
        
        body = "Your password reset link is: {link}".format(link=link)
        send_mail(
            "Password Reset from E-market",
            body,
            "emarket@gmail.com",
            [data['email']],
            fail_silently=False,
        )
        
        return Response({'details': 'Password reset sent to {email}'.format(email=data['email'])})
    
    except Exception as e:
        # Log the error message
        print(f"Error: {str(e)}")
        return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def reset_password(request, token):
    try:
        data = request.data
        user = get_object_or_404(User, profile__reset_password_token=token)
        if user.profile.reset_password_expire.replace(tzinfo=None) < datetime.now():
            return Response({'error': 'Token is expired'}, status=status.HTTP_400_BAD_REQUEST)
        if data['password'] != data['confirmPassword']:
            return Response({'error': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)
        
        user.password = make_password(data['password'])
        user.profile.reset_password_token = ""
        user.profile.reset_password_expire = None
        user.profile.save()
        user.save()
        return Response({'details': 'Password reset successfully'})
    except Exception as e:
        # Log the error message
        print(f"Error: {str(e)}")
        return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
