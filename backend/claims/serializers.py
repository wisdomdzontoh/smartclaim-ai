from rest_framework import serializers
from .models import Claim, Document

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'file', 'uploaded_at']

class ClaimSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    company = serializers.StringRelatedField(read_only=True)
    documents = DocumentSerializer(many=True, read_only=True)
    document_files = serializers.ListField(
        write_only=True,
        child=serializers.FileField(),
        required=False
    )

    class Meta:
        model = Claim
        fields = [
            'id', 'title', 'description',
            'status', 'priority', 'assigned_to',
            'ai_summary', 'ai_tags', 'severity_score', 'fraud_risk_score',
            'created_at', 'updated_at', 'resolved_at',
            'user', 'company',
            'documents', 'document_files',
        ]
        read_only_fields = ('user', 'company', 'created_at', 'updated_at', 'resolved_at')

    def create(self, validated_data):
        files = validated_data.pop('document_files', [])
        claim = Claim.objects.create(**validated_data)
        for f in files:
            Document.objects.create(claim=claim, file=f)
        return claim
