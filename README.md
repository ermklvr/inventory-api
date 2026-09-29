# API de Gestão de Inventário

API REST para gerenciamento de produtos, categorias e movimentações de estoque.

Projeto desenvolvido com foco em aprendizado prático de desenvolvimento backend, integração com banco de dados, regras de negócio, testes automatizados, migrations e containerização.

## Tecnologias

- Python 3.11
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic
- Alembic
- Pytest
- Docker
- Docker Compose

## Arquitetura

```text
Cliente
   ↓
FastAPI / Routers
   ↓
Schemas / Pydantic
   ↓
CRUD / Regras de negócio
   ↓
SQLAlchemy
   ↓
PostgreSQL
````

## Modelo de dados

```text
Category 1 ─── N Product 1 ─── N Movement
```

Principais tabelas:

* `categorias`
* `produtos`
* `movimentacoes`

## Funcionalidades

### Categorias

* Criar categoria
* Listar categorias
* Buscar categoria por ID
* Atualizar categoria
* Excluir categoria
* Impedir exclusão de categorias que possuem produtos

### Produtos

* Criar produto
* Listar produtos ativos
* Buscar produto por ID
* Atualizar produto
* Soft delete de produtos

### Movimentações

* Registrar entrada de estoque (`IN`)
* Registrar saída de estoque (`OUT`)
* Listar movimentações
* Buscar movimentação por ID
* Excluir movimentação
* Reverter o impacto no estoque ao excluir uma movimentação
* Impedir saídas maiores que o estoque disponível
* Impedir movimentações em produtos inativos

## Regras de negócio

* O preço dos produtos deve ser maior que zero.
* A quantidade de estoque não pode ser negativa.
* A quantidade de uma movimentação deve ser maior que zero.
* Um produto deve estar associado a uma categoria.
* Uma saída de estoque não pode resultar em estoque negativo.
* Produtos inativos não podem receber novas movimentações.
* A exclusão de produtos utiliza soft delete para preservar seu histórico.
* Categorias que possuem produtos não podem ser excluídas.
* A exclusão de uma movimentação reverte seu impacto no estoque.
* Movimentações não possuem atualização (`PUT`), preservando o histórico das operações.

## Tratamento de erros

A API utiliza exceções específicas para regras de negócio e retorna códigos HTTP apropriados.

* `404 Not Found` — recurso não encontrado
* `409 Conflict` — conflito com uma regra de negócio
* `422 Unprocessable Entity` — dados de entrada inválidos

## Como executar

### Pré-requisitos

* Python 3.11+
* Docker
* Docker Compose
* Git

### 1. Clonar o projeto

```bash
git clone https://github.com/ermklvr/inventory-api.git
cd inventory-api
```

### 2. Criar o arquivo `.env`

Crie um arquivo `.env` na raiz do projeto:

```env
DATABASE_URL=postgresql://admin:admin@localhost:5432/inventario
TEST_DATABASE_URL=postgresql://admin:admin@localhost:5432/inventario_test
```

### 3. Subir a aplicação

```bash
docker compose up --build -d
```

### 4. Executar as migrations

```bash
docker compose exec api alembic upgrade head
```

### 5. Criar o banco de testes

```bash
docker compose exec db psql -U admin -c "CREATE DATABASE inventario_test;"
```

### 6. Popular o banco com dados de exemplo

```bash
docker compose exec api python -m app.seed
```

### 7. Acessar a documentação

Swagger:

[http://localhost:8000/docs](http://localhost:8000/docs)

ReDoc:

[http://localhost:8000/redoc](http://localhost:8000/redoc)

## Testes

Os testes automatizados utilizam um banco PostgreSQL separado:

```text
inventario
    ↓
ambiente da aplicação

inventario_test
    ↓
pytest
```

Para executar os testes:

```bash
pytest -v
```

A suíte atual possui testes para:

* funcionamento da API;
* criação de produtos;
* validação de dados;
* soft delete;
* entradas de estoque;
* saídas de estoque;
* estoque insuficiente;
* produtos inativos;
* reversão de movimentações;
* CRUD de categorias;
* regras de integridade.

## Migrations

O projeto utiliza Alembic para controlar alterações na estrutura do banco de dados.

Aplicar migrations:

```bash
docker compose exec api alembic upgrade head
```

Criar uma nova migration:

```bash
docker compose exec api alembic revision --autogenerate -m "descricao_da_alteracao"
```

## Seed

O projeto possui uma seed para gerar uma base de demonstração com múltiplas categorias, produtos e movimentações.

Para executar:

```bash
docker compose exec api python -m app.seed
```

## Estrutura do projeto

```text
projeto-2/
│
├── alembic/
│   ├── versions/
│   ├── env.py
│   └── ...
│
├── app/
│   ├── crud/
│   ├── routers/
│   ├── exceptions/
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── main.py
│   └── seed.py
│
├── tests/
│   ├── conftest.py
│   └── test_products.py
│
├── .dockerignore
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── alembic.ini
├── pytest.ini
├── requirements.txt
└── README.md
```

## Banco de dados

A aplicação utiliza PostgreSQL.

A conexão é configurada através da variável de ambiente:

```env
DATABASE_URL=postgresql://admin:admin@localhost:5432/inventario
```

Quando a aplicação está dentro do Docker Compose, o PostgreSQL é acessado através do nome do serviço:

```text
db:5432
```

## Docker

O projeto utiliza Docker para padronizar o ambiente de execução.

Serviços:

```text
api
 ↓
FastAPI + Uvicorn

db
 ↓
PostgreSQL 16
```

Iniciar:

```bash
docker compose up --build -d
```

Verificar os containers:

```bash
docker compose ps
```

Parar:

```bash
docker compose down
```

## Endpoints

| Método | Endpoint           | Descrição              |
| ------ | ------------------ | ---------------------- |
| POST   | `/categories`      | Criar categoria        |
| GET    | `/categories`      | Listar categorias      |
| GET    | `/categories/{id}` | Buscar categoria       |
| PUT    | `/categories/{id}` | Atualizar categoria    |
| DELETE | `/categories/{id}` | Excluir categoria      |
| POST   | `/products`        | Criar produto          |
| GET    | `/products`        | Listar produtos ativos |
| GET    | `/products/{id}`   | Buscar produto         |
| PUT    | `/products/{id}`   | Atualizar produto      |
| DELETE | `/products/{id}`   | Desativar produto      |
| POST   | `/movements/`      | Criar movimentação     |
| GET    | `/movements/`      | Listar movimentações   |
| GET    | `/movements/{id}`  | Buscar movimentação    |
| DELETE | `/movements/{id}`  | Excluir movimentação   |

## Decisões de implementação

### Soft delete

Produtos não são removidos fisicamente do banco.

Em vez disso, o campo `active` é alterado para `False`, preservando o histórico do produto e suas movimentações.

### Movimentações sem PUT

Movimentações representam operações realizadas no estoque e funcionam como histórico.

Por isso, a API não permite editar uma movimentação existente.

Quando uma movimentação é excluída, seu impacto no estoque é revertido.

### Controle de concorrência

As operações de movimentação utilizam bloqueio de linha com `SELECT ... FOR UPDATE` através do SQLAlchemy:

```python
with_for_update()
```

Isso ajuda a evitar inconsistências quando múltiplas operações alteram o estoque simultaneamente.

### Transações

As operações de movimentação utilizam rollback em caso de erro:

```text
operação
   ↓
erro
   ↓
rollback
```

Dessa forma, alterações parciais não permanecem no banco.

## Objetivos do projeto

Este projeto foi desenvolvido para praticar:

* desenvolvimento de APIs REST;
* FastAPI;
* SQLAlchemy;
* PostgreSQL;
* modelagem relacional;
* Pydantic;
* validação de dados;
* migrations com Alembic;
* organização entre routers e CRUD;
* tratamento de exceções;
* regras de negócio;
* transações e rollback;
* controle de concorrência;
* soft delete;
* testes automatizados;
* fixtures com Pytest;
* banco de testes;
* Docker e Docker Compose.

## Status

Backend concluído, incluindo:

* modelagem;
* banco de dados;
* migrations;
* schemas;
* CRUD;
* regras de negócio;
* tratamento de erros;
* testes automatizados;
* ambiente Docker;
* seed;
* documentação.

```
```
