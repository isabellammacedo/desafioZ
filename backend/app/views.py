from rest_framework import viewsets
from .models import Company, Document, Signers
from .serializers import CompanySerializer, DocumentSerializer, SignersSerializer

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

class SignersViewSet(viewsets.ModelViewSet):
    queryset = Signers.objects.all()
    serializer_class = SignersSerializer