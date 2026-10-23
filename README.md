# University Health API

University Health is a REST API designed to centralize and provide structured information about university services and resources.

The API is intended to be consumed by different applications, such as web applications, mobile applications, administrative systems, or other services that need access to university information.

The project focuses on the backend and API layer, providing organized data, relationships between entities, validation, and HTTP endpoints through which client applications can access the information.

---

## Problem

University information and services are often distributed across different departments, offices, websites, and communication channels.

Students and other university users may need to search for information about services such as:

- Psychology
- Nursing
- Social Services
- Academic departments
- Careers
- University contacts
- Locations
- Schedules
- Available services

The purpose of University Health is to provide a centralized API that exposes this information in a structured and reusable way.

Instead of building an application tied to a single interface, the API can serve as a common backend for different applications.

---

## Project Goal

The main goal of University Health is to build a complete and well-structured REST API that provides university information through documented endpoints.

The API will allow client applications to retrieve and work with information about university services and other related entities.

The project will focus on:

- REST API design
- Data modeling
- Database relationships
- Request validation
- HTTP status codes
- CRUD operations where appropriate
- API documentation
- Containerized development
- Automated testing and CI
- Clean backend architecture

---

## Main Use Case

A client application should be able to consume the University Health API and request information without needing to know how the data is stored internally.

For example:

```text
Mobile Application
        |
        | HTTP Request
        v
+-------------------------+
|   University Health API |
|        FastAPI          |
+-------------------------+
        |
        v
+-------------------------+
|      PostgreSQL         |
+-------------------------+
```

---

## Cómo ejecutar

### Backend

```bash
cd backend
uv sync
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Rutas útiles:

- API: <http://localhost:8000>
- Documentación: <http://localhost:8000/docs>
- Health: <http://localhost:8000/health>
- Health versionado: <http://localhost:8000/api/v1/health>

> En el devcontainer usa siempre `uv run`. El comando `uvicorn` por sí solo
> no existe en el PATH porque las dependencias están dentro de `backend/.venv`.
> El `--host 0.0.0.0` permite que el navegador del host acceda al servidor.
>
> El `.venv` del devcontainer está aislado en un volumen de Docker. Si abres
> el proyecto directamente en Windows, elimina `backend/.venv` y ejecuta
> `uv sync` para crear el entorno de Windows.

### Frontend

```bash
cd frontend
pnpm install
pnpm dev
```

El frontend queda en <http://localhost:5173> y consume la API en
`http://localhost:8000/api/v1`.

