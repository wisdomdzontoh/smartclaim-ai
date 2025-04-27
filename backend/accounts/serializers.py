from rest_framework import serializers
from django.contrib.auth import get_user_model
from companies.models import Company
from companies.serializers import CompanySerializer

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    company_id = serializers.PrimaryKeyRelatedField(
        write_only=True, queryset=Company.objects.all(), source='company', required=False
    )

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'role', 'company', 'company_id',
            'phone_number', 'profile_picture', 'bio',
            'timezone', 'language', 'settings',
            'is_verified', 'two_factor_enabled',
            'date_joined', 'last_login',
        ]
        read_only_fields = ('date_joined', 'last_login')



class RegisterSerializer(serializers.ModelSerializer):
    password   = serializers.CharField(write_only=True)
    company_id = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.all(),
        source='company',
        write_only=True,
        required=True
    )

    class Meta:
        model  = User
        fields = [
          'username',
          'email',
          'password',
          'first_name',
          'last_name',
          'company_id',
        ]

    def create(self, validated_data):
        password = validated_data.pop('password')
        # will accept first_name, last_name, email, username, company
        user = User.objects.create_user(password=password, **validated_data)
        return user
