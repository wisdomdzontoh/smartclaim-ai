from rest_framework import serializers
from .models import Company

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')




# companies/serializers.py

from rest_framework import serializers
from .models import Company
from django.contrib.auth import get_user_model

User = get_user_model()

class CompanyRegistrationSerializer(serializers.Serializer):
    # Company fields
    name              = serializers.CharField(max_length=255)
    address           = serializers.CharField(required=False, allow_blank=True)
    contact_email     = serializers.EmailField(required=False, allow_blank=True)
    # initial admin user fields
    admin_username    = serializers.CharField(max_length=150)
    admin_email       = serializers.EmailField()
    admin_password    = serializers.CharField(write_only=True, min_length=8)

    def validate_admin_username(self, u):
        if User.objects.filter(username=u).exists():
            raise serializers.ValidationError("Username already taken")
        return u

    def create(self, validated_data):
        # 1) Create Company
        company = Company.objects.create(
            name          = validated_data.pop('name'),
            address       = validated_data.pop('address', ''),
            contact_email = validated_data.pop('contact_email', ''),
        )
        # 2) Create Admin User
        admin = User.objects.create_user(
            username = validated_data.pop('admin_username'),
            email    = validated_data.pop('admin_email'),
            password = validated_data.pop('admin_password'),
            role     = 'company_admin',
            company  = company
        )
        return {
            'company': company,
            'admin':   admin
        }
