from django.urls import path
from . import views

app_name = 'toll'

urlpatterns = [
    path('<str:gate_id>/', views.TollCaptureViewSet.as_view({'post': 'capture_vehicle'}), name='capture'),
]
