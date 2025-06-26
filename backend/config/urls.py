from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls), 
    path('api/', include('core.api.urls')), # Central de API

    # Duas linhas para autenticação:
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('accounts/', include('django.contrib.auth.urls')), # PÁGINAS DE LOGIN/LOGOUT
    path('', include('core.urls')), # Nossa página inicial
]