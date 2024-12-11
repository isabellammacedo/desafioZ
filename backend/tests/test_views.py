import pytest
from rest_framework.test import APIClient
from rest_framework import status
from app.models import Company, Document, Signers
from unittest.mock import patch


@pytest.fixture
def create_company():
    return Company.objects.create(
        name="Nome Usuario",
        api_token="token1234"
    )


@pytest.fixture
def create_document(create_company):
    document = Document.objects.create(
        openID=123,
        name="Documento 1",
        company=create_company,
        status="em-curso",
        token="token 5432"
    )
    return document


@pytest.fixture
def create_signer(create_document):
    signer = Signers.objects.create(
        document=create_document,
        name="Signatário 1",
        email="teste@teste.com",
        token="token54325",
        status="novo"
    )
    return signer


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_get_documents(api_client, create_document, create_signer):
    url = "/api/docs/"
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    document_data = response.data[0]
    assert 'signers' in document_data
    assert len(document_data['signers']) == 1
    assert document_data['signers'][0]['name'] == "Signatário 1"


@pytest.mark.django_db
def test_post_document_no_api_token(api_client, create_company):
    create_company.api_token = ""
    create_company.save()

    url = "/api/docs/"
    data = {
        "openID": 123,
        "name": "Documento 3"
    }

    response = api_client.post(url, data, format='json')

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.data['error'] == "API token não encontrado"


@pytest.mark.django_db
def test_put_document(api_client, create_document, create_signer):
    url = f"/api/docs/{create_document.id}/"
    data = {
        "name": "Documento atualizado",
        "signers": [
            {"id": create_signer.id, "name": "Signatário editado", "email": "teste3@teste.com"}
        ]
    }

    response = api_client.put(url, data, format='json')

    assert response.status_code == status.HTTP_200_OK
    assert response.data['message'] == "Documento atualizado com sucesso!"
    create_document.refresh_from_db()
    assert create_document.name == "Documento atualizado"
    create_signer.refresh_from_db()
    assert create_signer.name == "Signatário editado"
    assert create_signer.email == "teste3@teste.com"


@pytest.mark.django_db
def test_delete_document_to_remove_document(api_client, create_document, create_signer):
    url = f"/api/docs/{create_document.id}/"

    response = api_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Document.objects.count() == 0
    assert Signers.objects.count() == 0


@pytest.mark.django_db
def test_delete_document_not_found(api_client):
    url = "/api/docs/999999/"
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert 'error' in response.data
    assert response.data['error'] == "Documento não encontrado"


@pytest.mark.django_db
@patch("requests.post")
def test_post_document_success(mock_post, api_client, create_company):
    
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"status": "em-curso"}
    
    url = "/api/docs/"
    data = {
        "openID": 123,
        "name": "Documento 4",
        "signers": [
            {"name": "Signatário Teste 1", "email": "testesig@teste.com"},
            {"name": "Signatário Teste 2", "email": "testesig2@teste.com"}
        ]
    }

    response = api_client.post(url, data, format='json')

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['message'] == "Documento criado com sucesso!"
    assert 'document_id' in response.data

    assert Document.objects.count() == 1
    assert Document.objects.first().name == "Documento 4"
    assert Signers.objects.count() == 2

@pytest.mark.django_db
def test_delete_document_to_remove_document(api_client, create_document, create_signer):
    url = f"/api/docs/{create_document.id}/"
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Document.objects.filter(id=create_document.id).exists()
    assert not Signers.objects.filter(document_id=create_document.id).exists()