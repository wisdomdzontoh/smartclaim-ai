from rest_framework import viewsets
from django.contrib.auth import get_user_model
from accounts.permissions import IsSuperAdmin
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .serializers import RegisterSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated



User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.select_related('company').all()
    serializer_class = UserSerializer
    permission_classes = [IsSuperAdmin]  # only superadmin can CRUD users




class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Return the authenticated user’s profile.
        """
        serializer = UserSerializer(request.user)
        return Response(serializer.data)





class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # now issue tokens
        token_serializer = TokenObtainPairSerializer(
            data={
              'username': request.data['username'],
              'password': request.data['password']
            }
        )
        token_serializer.is_valid(raise_exception=True)
        tokens = token_serializer.validated_data

        return Response(
            {
              'user': UserSerializer(user).data,
              'access':  tokens['access'],
              'refresh': tokens['refresh'],
            },
            status=status.HTTP_201_CREATED
        )
