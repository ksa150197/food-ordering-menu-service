# Food Ordering System – Menu Service

A RESTful microservice for managing food items in the Food Ordering and Management System. Developed using **Python FastAPI**, **SQLAlchemy**, and **PostgreSQL**.

## 1. Project Overview

The Menu Service is responsible for maintaining the food catalogue of the Food Ordering System. It provides REST APIs to create, retrieve, update, delete, and manage the availability of food items.

This service operates independently and owns its data. Other microservices access menu information through its exposed REST APIs rather than accessing its database directly.

## 2. Key Features

- Create new food items.
- Retrieve all food items.
- Retrieve an individual food item using its ID.
- Update existing food item details.
- Delete food items.
- Update food item availability.
- Filter food items based on availability.
- Health-check endpoint for service monitoring.
- Automatic API documentation through FastAPI Swagger UI.

## 3. Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.12 | Programming language |
| FastAPI 0.115.12 | REST API framework |
| SQLAlchemy 2.0.40 | Database ORM |
| Pydantic 2.11.3 | Request and response validation |
| PostgreSQL | Persistent database |
| SQLite | Local development fallback |
| Docker | Containerisation |
| Uvicorn 0.34.0 | ASGI application server |

## 4. Project Structure

```text
menu-service/
│
├── app/
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   └── database.py
│
├── Dockerfile
├── requirements.txt
└── README.md
```

### Application Components

- **main.py:** Defines REST endpoints and implements menu management operations.
- **models.py:** Defines the SQLAlchemy database model for food items.
- **schemas.py:** Defines Pydantic models for request validation and API responses.
- **database.py:** Configures the database connection and SQLAlchemy sessions.
- **Dockerfile:** Defines how the Menu Service container image is built.

## 5. Database Design

The Menu Service maintains its own database named `menu_db` in the PostgreSQL deployment.

The food item records contain the following attributes:

| Attribute | Description |
|---|---|
| id | Unique food item identifier |
| name | Name of the food item |
| description | Food item description |
| price | Price of the food item |
| category | Food category |
| available | Availability status |

The service uses its own database connection and does not directly access the Order Service database.

## 6. API Endpoints

The service exposes the following REST APIs:

| HTTP Method | Endpoint | Description |
|---|---|---|
| POST | `/menu/items` | Create a food item |
| GET | `/menu/items` | Retrieve all food items |
| GET | `/menu/items?available_only=true` | Retrieve available items |
| GET | `/menu/items/{item_id}` | Retrieve an individual item |
| PUT | `/menu/items/{item_id}` | Update food item details |
| PATCH | `/menu/items/{item_id}/availability?available=true` | Update availability |
| DELETE | `/menu/items/{item_id}` | Delete a food item |
| GET | `/health` | Check service health |

### Example: Create a Food Item

**Request**

```http
POST /menu/items
Content-Type: application/json
```

```json
{
  "name": "Paneer Wrap",
  "description": "Grilled paneer with fresh vegetables",
  "price": 149.00,
  "category": "Wraps",
  "available": true
}
```

**Expected response:** `201 Created`

```json
{
  "id": 1,
  "name": "Paneer Wrap",
  "description": "Grilled paneer with fresh vegetables",
  "price": 149.0,
  "category": "Wraps",
  "available": true
}
```

## 7. Local Setup and Execution

### Prerequisites

- Python 3.12 or later.
- pip package manager.
- Git.

### Step 1: Clone the repository

```bash
git clone https://github.com/ksa150197/food-ordering-menu-service.git
cd food-ordering-menu-service
```

### Step 2: Create a virtual environment

```bash
python3 -m venv .venv
```

Activate it on macOS/Linux:

```bash
source .venv/bin/activate
```

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Start the service

```bash
uvicorn app.main:app --reload --port 8000
```

If `DATABASE_URL` is not configured, the service uses a local SQLite database named `menu.db`.

For PostgreSQL, configure the `DATABASE_URL` environment variable before starting the service.

Example:

```bash
export DATABASE_URL="postgresql+psycopg://fooduser:foodpass@localhost:5432/menu_db"
```

### Step 5: Access API documentation

Open the following URL:

http://localhost:8000/docs

The Swagger UI allows users to interactively execute and test the available APIs.

## 8. Docker Deployment

Build the Docker image from the repository root:

```bash
docker build -t food-menu-service:latest .
```

Run the container:

```bash
docker run -d \
  --name menu-service \
  -p 8000:8000 \
  -e DATABASE_URL="postgresql+psycopg://fooduser:foodpass@host.docker.internal:5432/menu_db" \
  food-menu-service:latest
```

The PostgreSQL server must be reachable from the container using the configured hostname and credentials.

Verify the container:

```bash
docker ps
```

Access Swagger UI:

http://localhost:8000/docs

## 9. Kubernetes Deployment

The Menu Service was deployed to a local Kubernetes cluster using Minikube.

The deployment configuration defines:

- A Kubernetes Deployment with one replica.
- A Kubernetes Service for network access.
- A container image named `food-menu-service:latest`.
- A PostgreSQL database connection.
- A readiness probe using the `/health` endpoint.

The Kubernetes manifests are maintained separately in the main project deployment directory.

The service is internally accessible through Kubernetes DNS:

```text
http://menu-service:8000
```

## 10. Health Check

The service provides a health-check endpoint:

```http
GET /health
```

Example response:

```json
{
  "service": "menu-service",
  "status": "healthy"
}
```

This endpoint is also used by the Kubernetes readiness probe.

## 11. Repository

GitHub: https://github.com/ksa150197/food-ordering-menu-service

## 12. Project Scope

This microservice was developed as part of an individual Scalable Services assignment to demonstrate:

- Microservice development using FastAPI.
- REST API implementation.
- Independent database ownership.
- CRUD operations.
- Docker containerisation.
- Kubernetes deployment using Minikube.

This is an academic demonstration project and is not intended as a production-hardened application.