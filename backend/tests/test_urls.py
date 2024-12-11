import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from app.models import Company, Document, Signers

@pytest.fixture
def company():
    return Company.objects.create(
        name="Usuário para testes", 
        api_token="abcdefg"
    )

@pytest.fixture
def document(company):
    return Document.objects.create(
        name="Documento para testes", 
        token="abc1", 
        status="em-curso", 
        company=company, 
        openID=1
    )

@pytest.fixture
def signer(document):
    return Signers.objects.create(
        token="1234",
        status="novo",
        name="Signatário 1",
        email="teste@teste.com",
        document=document
    )

@pytest.mark.django_db
def test_api_company_list_view(company):
    url = reverse('company-list')
    response = APIClient().get(url)
    assert response.status_code == 200
    assert len(response.data) > 0
    assert response.data[0]['name'] == "Usuário para testes"

@pytest.mark.django_db
def test_api_company_detail_view(company):
    url = reverse('company-detail', args=[company.pk])
    response = APIClient().get(url)
    assert response.status_code == 200
    assert response.data['name'] == "Usuário para testes"
    assert response.data['api_token'] == "abcdefg"

@pytest.mark.django_db
def test_api_document_list_view(document):
    url = reverse('document-list')
    response = APIClient().get(url)
    assert response.status_code == 200
    assert len(response.data) > 0
    assert response.data[0]['name'] == "Documento para testes"

@pytest.mark.django_db
def test_api_document_detail_view(document):
    url = reverse('document-detail', args=[document.pk])
    response = APIClient().get(url)
    assert response.status_code == 200
    assert response.data['name'] == "Documento para testes"
    assert response.data['status'] == "em-curso"

@pytest.mark.django_db
def test_api_signer_view(signer):
    url = reverse('signers-list')
    response = APIClient().get(url)
    assert response.status_code == 200
    assert len(response.data) > 0
    assert response.data[0]['name'] == "Signatário 1"

@pytest.mark.django_db
def test_api_signer_detail_view(signer):
    url = reverse('signers-detail', args=[signer.pk])
    response = APIClient().get(url)
    assert response.status_code == 200
    assert response.data['name'] == "Signatário 1"
    assert response.data['email'] == "teste@teste.com"

def test_swagger_ui():
    url = reverse('swagger-ui')
    response = APIClient().get(url)
    assert response.status_code == 200
