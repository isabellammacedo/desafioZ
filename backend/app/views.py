from rest_framework import viewsets
from .models import Company, Document, Signers
from .serializers import CompanySerializer, DocumentSerializer, SignersSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests

class CompanyViewSet(viewsets.ModelViewSet):
    """
    Dados da conta da empresa.
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

class DocumentView(APIView):
    """
    Listar, criar, atualizar e excluir documentos.
    """

    def get(self, request):
        documents = Document.objects.all()
        documents_data = []

        for document in documents:
            signers = Signers.objects.filter(document=document)
            signers_data = SignersSerializer(signers, many=True).data
            document_data = DocumentSerializer(document).data
            document_data['signers'] = signers_data
            documents_data.append(document_data)

        return Response(documents_data)

    def post(self, request):

        company = Company.objects.first()
        if not company or not company.api_token:
            return Response(
                {"error": "API token não encontrado"}, 
                status=status.HTTP_403_FORBIDDEN
            )

        api_token = company.api_token
        document_data = request.data

        api_ZapSign = "https://sandbox.api.zapsign.com.br/api/v1/docs/"
        headers = {"Authorization": f"Bearer {api_token}"}

        try:
            api_response = requests.post(api_ZapSign, json=document_data, headers=headers)
            api_response.raise_for_status()
            api_response_data = api_response.json()
        except requests.exceptions.RequestException as e:
            return Response(
                {"error": f"Erro na API externa: {str(e)}"}, 
                status=status.HTTP_400_BAD_REQUEST
            )


        document = Document.objects.create(
            openID=document_data.get('openID', 0),
            token=api_token,
            name=document_data['name'],
            status=api_response_data.get('status', 'em-curso'),
            externalID=api_response_data.get('external_id', ''),
            company=company,
        )


        for signer in document_data.get('signers', []):
            Signers.objects.create(
                document=document,
                name=signer['name'],
                email=signer.get('email', ''),
                externalID=api_response_data.get('external_id', ''),
                token=api_token,
                status='novo'
            )

        return Response(
            {"message": "Documento criado com sucesso!", "document_id": document.id}, 
            status=status.HTTP_201_CREATED
        )
    
    def put(self, request, pk):
        document = Document.objects.get(pk=pk)
        document.name = request.data.get('name', document.name)
        document.save()

        for signer_data in request.data.get('signers', []):
            signer = Signers.objects.get(id=signer_data['id'], document=document)
            signer.name = signer_data['name']
            signer.email = signer_data['email']
            signer.save()

        return Response({"message": "Documento atualizado com sucesso!"}, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        try:
            document = Document.objects.get(pk=pk)
            signers = Signers.objects.filter(document=document)
            signers.delete()
            document.delete()
            return Response({"message": "Documento e signatários excluídos com sucesso!"}, status=status.HTTP_204_NO_CONTENT)
        except Document.DoesNotExist:
            return Response({"error": "Documento não encontrado"}, status=status.HTTP_404_NOT_FOUND)