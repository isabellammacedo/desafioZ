import pytest
from app.models import Company, Document, Signers

@pytest.mark.django_db
def test_create_company():
    company = Company.objects.create(
        name="Conta teste",
        api_token="token12345"
    )
    assert company.name == "Conta teste"
    assert company.api_token == "token12345"
    assert company.created_at is not None
    assert company.last_updated_at is not None

@pytest.mark.django_db
def test_create_document():
    company = Company.objects.create(
        name="Conta teste",
        api_token="token12345"
    )

    document = Document.objects.create(
        openID=12345,
        token="token5678",
        name="Documento 1",
        status="em-curso",
        company=company
    )

    assert document.name == "Documento 1"
    assert document.status == "em-curso"
    assert document.company == company
    assert document.created_at is not None
    assert document.last_updated_at is not None
    assert document.externalID is None

@pytest.mark.django_db
def test_create_signer():
    company = Company.objects.create(
        name="Conta teste",
        api_token="token12345"
    )

    document = Document.objects.create(
        openID=12345,
        token="token5678",
        name="Documento 1",
        status="em-curso",
        company=company
    )

    signer = Signers.objects.create(
        token="token54321",
        status="novo",
        name="Signatário abc",
        email="teste@teste2.com",
        document=document
    )

    assert signer.name == "Signatário abc"
    assert signer.email == "teste@teste2.com"
    assert signer.status == "novo"
    assert signer.document == document
    assert signer.externalID is None

@pytest.mark.django_db
def test_company_str_method():
    company = Company.objects.create(
        name="Conta teste",
        api_token="token12345"
    )
    assert str(company) == company.name

@pytest.mark.django_db
def test_document_str_method():
    company = Company.objects.create(
        name="Conta teste",
        api_token="token12345"
    )
    document = Document.objects.create(
        openID=12345,
        token="token5678",
        name="Documento 1",
        status="em-curso",
        company=company
    )
    assert str(document) == document.name

@pytest.mark.django_db
def test_signer_str_method():
    company = Company.objects.create(
        name="Conta teste",
        api_token="token12345"
    )
    document = Document.objects.create(
        openID=12345,
        token="token5678",
        name="Documento 1",
        status="em-curso",
        company=company
    )
    signer = Signers.objects.create(
        token="token54321",
        status="novo",
        name="Signatário abc",
        email="teste@teste2.com",
        document=document
    )
    assert str(signer) == signer.name

@pytest.mark.django_db
def test_company_auto_timestamp():
    company = Company.objects.create(
        name="Conta teste",
        api_token="token12345"
    )
    initial_created_at = company.created_at
    initial_updated_at = company.last_updated_at

    company.name = "Edit Company"
    company.save()

    assert company.created_at == initial_created_at
    assert company.last_updated_at > initial_updated_at

@pytest.mark.django_db
def test_document_auto_timestamp():
    company = Company.objects.create(
        name="Conta teste",
        api_token="token12345"
    )
    document = Document.objects.create(
        openID=12345,
        token="token5678",
        name="Documento 1",
        status="em-curso",
        company=company
    )
    initial_created_at = document.created_at
    initial_updated_at = document.last_updated_at

    document.status = "assinado"
    document.save()

    assert document.created_at == initial_created_at
    assert document.last_updated_at > initial_updated_at
