from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'users'

# Router for users endpoints
user_router = DefaultRouter()
user_router.register(r'', views.UserViewSet, basename='user')
user_router.register(r'auth', views.AuthViewSet, basename='auth')

urlpatterns = [
    path('', include(user_router.urls)),
]
