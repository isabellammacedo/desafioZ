# Desafio Técnico - CRUD de Documentos

Este desafio consiste em desenvolver um CRUD (Create, Read, Update, Delete) que permita cadastrar, listar, editar e deletar documentos e seus signatários. A aplicação envolve tanto o frontend quanto o backend, com integração entre eles utilizando banco de dados, Docker e Docker Compose.

## Tecnologias utilizadas

### Frontend:
- **Angular** (para desenvolvimento da interface)
- **Typescript** (linguagem utilizada no desenvolvimento frontend)

### Backend:
- **Django** (framework Python)
- **Pytest** (para os testes)

### Banco de Dados:
- **PostgreSQL** (utilizado como banco de dados relacional)

### Contêineres:
- **Docker** (para criar ambientes isolados)
- **Docker Compose** (para gerenciar os contêineres)

## Pré-requisitos:

É necessário ter instalado na máquina:
- Docker
- Docker Compose

## Passos para rodar o projeto:

1. Clone o repositório para sua máquina local.

2. No terminal, na raiz do projeto, execute o comando:
`docker compose up --build`

Durante o processo de build, o Django irá realizar as migrations e criar um usuário administrador para acesso ao painel administrativo do Django.

## Acessos depois do build:

O sistema ficará disponível nas seguintes portas:

- Frontend (Angular): http://localhost:4200
- Backend (Django API): http://localhost:8000
- Admin do Django: http://localhost:8000/admin
- Documentação da API (Swagger): http://localhost:8000/swagger/
- Endpoints da API: http://localhost:8000/api/


Para integrar a aplicação à API externa, é necessário cadastrar o token, conforme abaixo.

### Passos para configurar o token:
Crie uma conta na plataforma ZapSign (https://www.zapsign.com.br/).  
Obtenha o API Token gerado para a sua conta. Este token geralmente pode ser encontrado nas configurações de API da plataforma.  
Entre em http://localhost:8000/admin com as credenciais:  
Usuário: `admin`  
Senha: `admin`  

No painel admin, acesse Company.  
Adicione o Nome da empresa e o API Token obtido na ZapSign.  
Após configurar o token, o sistema estará pronto para fazer requisições à API externa da ZapSign.  