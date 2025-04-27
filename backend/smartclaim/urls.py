"""
URL configuration for smartclaim project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from companies.views import CompanyViewSet, CompanyRegisterView
from accounts.views import UserViewSet, UserProfileView, RegisterView
from claims.views import ClaimViewSet

router = DefaultRouter()
router.register(r'companies', CompanyViewSet)
router.register(r'users', UserViewSet)
router.register(r'claims', ClaimViewSet)


urlpatterns = [
    path('api/companies/register/', CompanyRegisterView.as_view(), name='company-register'),
    path('admin/', admin.site.urls),
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/users/me/', UserProfileView.as_view(), name='user-profile'),
    path('api/auth/register/', RegisterView.as_view(), name='auth-register'),
    
    path('api/', include(router.urls)),
]



