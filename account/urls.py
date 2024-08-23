from django.urls import path
from .views import register, forgot_password, reset_password

urlpatterns = [
    path('register/', register, name='register'),
    path('forgot_password/', forgot_password, name='forgot_password'),
    path('reset_password/<str:token>/', reset_password, name='reset_password'),
]
