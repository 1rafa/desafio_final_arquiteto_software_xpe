# Desafio final Arquiteto Software XPEducação

## Descrição

Este projeto é a solução para o Desafio Final do bootcamp do curso de pós-graduação em Arquitetura de Software na XPEducação. A aplicação consiste em uma API REST para gerenciamento de clientes, implementando operações CRUD (Create, Read, Update, Delete) conforme o padrão arquitetural MVC (Model-View-Controller).

A API foi desenvolvida utilizando **Python** com a biblioteca **FastAPI**, enquanto a persistência de dados foi realizada com **SQLite** via **SQLAlchemy**.

## Tecnologias Utilizadas

- **Python 3.x**
- **FastAPI** (Framework para desenvolvimento da API)
- **SQLAlchemy** (ORM para interação com o banco de dados SQLite)
- **Uvicorn** (Servidor ASGI para execução da API)
- **Pydantic** (Validação e tipagem de dados)
- **pytest** e **FastAPI TestClient** (Testes automatizados)

## Instalação e Configuração

1. Clone o repositório:

   ```sh
   git clone https://github.com/1rafa/desafio_final_arquiteto_software_xpe.git
   cd customer-api
   ```

2. Crie um ambiente virtual (opcional, mas recomendado):

   ```sh
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate  # Windows
   ```

3. Instale as dependências:

   ```sh
   pip install -r requirements.txt
   ```

## Execução da API

Para iniciar o servidor, execute:

```sh
fastapi run  src/main.py
```
### Documentação Automática

FastAPI gera automaticamente uma documentação interativa acessível nos seguintes endpoints:

- **Swagger UI:** [http://0.0.0.0:8000/docs](http://127.0.0.1:8000/docs)
- **Redoc:** [http://0.0.0.0:8000/redoc](http://127.0.0.1:8000/redoc)

## Endpoints Disponíveis

### Criar um Cliente

```http
POST /customers/
```

#### Corpo da requisição (JSON):

```json
{
  "name": "João Silva",
  "email": "joao@example.com",
  "phone": "99999-9999"
}
```

### Buscar Todos os Clientes

```http
GET /customers/
```

### Buscar Cliente por ID

```http
GET /customers/{customer_id}
```

### Atualizar um Cliente

```http
PUT /customers/{customer_id}
```

#### Corpo da requisição (JSON):

```json
{
  "name": "João Souza",
  "email": "joaosouza@example.com",
  "phone": "98888-8888"
}
```

### Deletar um Cliente

```http
DELETE /customers/{customer_id}
```

### Contar o Número de Clientes

```http
GET /customers/count
```

## Testes

Os testes foram desenvolvidos utilizando `pytest`. Para executá-los, utilize o seguinte comando:

```sh
pytest
```

Isso irá rodar os testes automatizados definidos no diretório `tests/`.
