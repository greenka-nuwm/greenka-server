"""greenka URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken import views

import tree.views as tree_views


urlpatterns = [
    path(r'api-auth/', include('rest_framework.urls')),
    path(r'admin/', admin.site.urls),
    path(r'user/', include('gauth.urls')),
    path(r'trees/', include('tree.urls')),
    path(r'problems/', include('problems.urls')),
    path(r'polygons/', include('polygon.urls')),
    path(r'token/', views.obtain_auth_token),
    path(r'auth/', include('rest_framework_social_oauth2.urls')),
]
