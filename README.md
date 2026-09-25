# E-Commerce Admin Backend API

A REST API for managing an e-commerce admin panel.

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- JWT Authentication
- Swagger / OpenAPI

## Features

- Admin JWT authentication
- Brand CRUD
- Category CRUD
- Subcategory CRUD
- Product CRUD
- Product Variant CRUD
- Product relationships
- Request/response validation
- Product pagination
- Swagger API documentation

## Project Structure

```text
Ecommerce_admin/
│
├── app/
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── database.py
│   ├── auth.py
│   └── __init__.py
│
├── ecommerce.db
├── requirements.txt
└── README.md