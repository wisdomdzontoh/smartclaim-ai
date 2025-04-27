from django.contrib import admin
from .models import Claim, Document

class DocumentInline(admin.TabularInline):
    model = Document
    extra = 0
    readonly_fields = ('uploaded_at',)

@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'user', 'company',
        'status', 'priority', 'created_at', 'resolved_at'
    )
    list_filter = ('status', 'priority', 'company')
    search_fields = ('title', 'description', 'user__username', 'company__name')
    readonly_fields = ('created_at', 'updated_at', 'resolved_at')
    inlines = [DocumentInline]

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('file', 'claim', 'uploaded_at')
    search_fields = ('file',)
    readonly_fields = ('uploaded_at',)
