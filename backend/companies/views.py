from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Company
from .serializers import CompanySerializer
from accounts.permissions import IsSuperAdmin, IsCompanyAdminOrReadOnly

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated, IsCompanyAdminOrReadOnly | IsSuperAdmin]



# companies/views.py

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import CompanyRegistrationSerializer
from .models import Company
from accounts.serializers import UserSerializer
from .serializers import CompanySerializer  # <— your ModelSerializer for Company
from django.contrib.auth import get_user_model

User = get_user_model()

class CompanyRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Public endpoint: register a new insurance firm + its first Company Admin.
        """
        reg_serializer = CompanyRegistrationSerializer(data=request.data)
        reg_serializer.is_valid(raise_exception=True)

        result = reg_serializer.save()
        company = result['company']
        admin   = result['admin']

        # Generate tokens for the new admin
        refresh = RefreshToken.for_user(admin)

        # Serialize them properly
        company_data = CompanySerializer(company).data
        admin_data   = UserSerializer(admin).data

        return Response({
            'company': company_data,
            'admin':   admin_data,
            'access':  str(refresh.access_token),
            'refresh': str(refresh),
        }, status=status.HTTP_201_CREATED)

