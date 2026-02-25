from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from users.views import WalletViewSet

def home(request):
    return HttpResponse("Welcome to AutoFare - Toll Collection System API")

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    # API endpoints - following contract structure
    path('api/users/', include('users.urls')),
    path('api/user/car', include('vehicles.urls')),
    path('api/user/wallet', WalletViewSet.as_view({'get': 'list', 'post': 'create'}), name='wallet'),
    path('api/capture/', include('toll.urls')),
    # Legacy app routes
    path('trips/', include('trips.urls')),
    path('payment/', include('payment.urls')),
    path('ai/', include('ai.urls')),
    path('vehicles/', include('vehicles.urls')),
    path('violations/', include('violations.urls')),
    path('notifications/', include('notifications.urls')),
    path('adminelweb/', include('Adminelweb.urls')),
]
