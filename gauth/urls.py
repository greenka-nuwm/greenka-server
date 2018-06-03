from django.urls import path
from gauth.views import get_self, register


urlpatterns = [
    path('self', get_self),
    path('register', register),
]