from rest_framework import viewsets
from .models import Company, Document, Signers
from .serializers import CompanySerializer, DocumentSerializer, SignersSerializer

class CompanyViewSet(viewsets.ModelViewSet):
    """
    Dados da empresa.
    """
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

class DocumentViewSet(viewsets.ModelViewSet):
    """
    Documentos criados via API ZapSign.
    """
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

class SignersViewSet(viewsets.ModelViewSet):
    """
    Signatários associados a cada documento.
    """
    queryset = Signers.objects.all()
    serializer_class = SignersSerializer