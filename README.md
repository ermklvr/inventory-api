# API de Gestão de Inventário

API REST para gerenciamento de categorias, produtos e movimentações de estoque.

## Tecnologias

Python, FastAPI, SQLAlchemy, PostgreSQL, Alembic, Pytest e Docker.

## Executar

**Pré-requisitos:** Docker, Docker Compose e Python 3.11+.

```bash
git clone https://github.com/guto-henrique/inventory-api.git

cd inventory-api

docker compose up --build -d

docker compose exec api alembic upgrade head
```

A API estará disponível em `http://localhost:8000`.

Para carregar dados de exemplo:

```bash
docker compose exec api python -m app.seed
```

## Documentação

* [Swagger UI](http://localhost:8000/docs)
* [ReDoc](http://localhost:8000/redoc)

## Testes

Configure o banco de testes no arquivo `.env`:

```env
TEST_DATABASE_URL=postgresql://admin:admin@localhost:5432/inventario_test
```

Execute:

```bash
pytest -v
```

## Endpoints

| Recurso       | Operações                                            |
| ------------- | ---------------------------------------------------- |
| Categorias    | `POST`, `GET`, `GET/{id}`, `PUT/{id}`, `DELETE/{id}` |
| Produtos      | `POST`, `GET`, `GET/{id}`, `PUT/{id}`, `DELETE/{id}` |
| Movimentações | `POST`, `GET`, `GET/{id}`, `DELETE/{id}`             |

## Regras principais

* O estoque não pode ficar negativo.
* Produtos inativos não recebem movimentações.
* Categorias com produtos não podem ser excluídas.
* Produtos utilizam soft delete.
* Movimentações não podem ser editadas.
* A exclusão de uma movimentação reverte o estoque.

Para parar a aplicação:

```bash
docker compose down
```
