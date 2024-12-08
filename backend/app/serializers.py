from app.models import Company, Document, Signers
from rest_framework import serializers


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'

class SignersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Signers
        fields = '__all__'