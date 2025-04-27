from django.contrib import admin
from .models import Company

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'contact_email', 'industry',
        'subscription_plan', 'is_active', 'created_at'
    )
    list_filter = ('subscription_plan', 'is_active', 'industry')
    search_fields = ('name', 'contact_email', 'website')
    readonly_fields = ('created_at', 'updated_at')
