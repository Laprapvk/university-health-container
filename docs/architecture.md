# University Health — Architecture & Data Model

## 1. Project Overview

University Health is a backend REST API designed to provide structured university information through a centralized service.

The API is intended to be consumed by different client applications, such as:

- Web applications
- Mobile applications
- University portals
- Administrative systems
- Chatbots or virtual assistants
- Other internal or external services

The project focuses on the backend and API layer rather than building a specific frontend application.

The API will provide information about university services, departments, campuses, buildings, staff, contact information, schedules, and other useful university resources.

---

# 2. Architecture

The project follows a layered backend architecture.

```text
                         ┌─────────────────────────┐
                         │      API Clients         │
                         │                         │
                         │ Web / Mobile / Other    │
                         └────────────┬────────────┘
                                      │
                                      │ HTTP / REST
                                      ▼
                         ┌─────────────────────────┐
                         │       FastAPI API       │
                         │                         │
                         │ Routes / Endpoints      │
                         └────────────┬────────────┘
                                      │
                                      ▼
                         ┌─────────────────────────┐
                         │      Service Layer      │
                         │                         │
                         │ Business Logic          │
                         └────────────┬────────────┘
                                      │
                                      ▼
                         ┌─────────────────────────┐
                         │    Data Access Layer    │
                         │                         │
                         │ Database Operations     │
                         └────────────┬────────────┘
                                      │
                                      ▼
                         ┌─────────────────────────┐
                         │      PostgreSQL         │
                         │                         │
                         │ University Data         │
                         └─────────────────────────┘
```

---

# 3. Technology Stack

## Backend

- Python
- FastAPI
- Pydantic
- Uvicorn

## Database

- PostgreSQL

## Development Environment

- Docker
- Docker Compose
- Dev Containers
- VS Code

## Development Tools

- Git
- GitHub
- GitHub Actions
- Ruff
- Prettier
- ESLint

---

# 4. Backend Architecture

The backend is organized into different responsibilities.

```text
backend/
│
├── app/
│   ├── main.py
│   │
│   ├── api/
│   │   └── routes/
│   │
│   ├── models/
│   │
│   ├── schemas/
│   │
│   ├── services/
│   │
│   ├── repositories/
│   │
│   ├── core/
│   │
│   └── db/
│
├── pyproject.toml
└── uv.lock
```

## Responsibilities

### `main.py`

Application entry point.

Responsible for creating the FastAPI application and registering API routes.

### `api/routes/`

Contains HTTP endpoints.

Example:

```text
GET    /api/v1/campuses
GET    /api/v1/campuses/{id}

GET    /api/v1/departments
GET    /api/v1/departments/{id}

GET    /api/v1/services
GET    /api/v1/services/{id}
```

### `models/`

Contains database models representing the entities stored in PostgreSQL.

### `schemas/`

Contains Pydantic schemas used for request validation and API responses.

### `services/`

Contains business logic.

The service layer prevents business rules from being placed directly inside API routes.

### `repositories/`

Responsible for database access.

Repositories provide an abstraction between the business logic and PostgreSQL.

### `core/`

Contains application-wide configuration and shared functionality.

Possible responsibilities include:

- Configuration
- Authentication
- Authorization
- Security
- Environment variables

### `db/`

Contains database configuration and database connection logic.

---

# 5. Data Modeling

The database represents the structure of a university and the resources available to students and other users.

The main entities are:

1. University
2. Campus
3. Building
4. Department
5. Service
6. Staff Member
7. Contact
8. Schedule
9. User
10. Role

---

# 6. Entity Relationship Diagram

```mermaid
erDiagram

    UNIVERSITY ||--o{ CAMPUS : has

    CAMPUS ||--o{ BUILDING : contains

    CAMPUS ||--o{ DEPARTMENT : contains

    DEPARTMENT ||--o{ SERVICE : provides

    DEPARTMENT ||--o{ STAFF_MEMBER : employs

    SERVICE ||--o{ CONTACT : has

    SERVICE ||--o{ SCHEDULE : has

    BUILDING ||--o{ SERVICE : hosts

    USER }o--|| ROLE : has

    UNIVERSITY {
        int id PK
        string name
        string description
        string website
        string email
        string phone
    }

    CAMPUS {
        int id PK
        int university_id FK
        string name
        string address
        string city
        string state
        string postal_code
        string phone
    }

    BUILDING {
        int id PK
        int campus_id FK
        string name
        string code
        string address
        string description
    }

    DEPARTMENT {
        int id PK
        int campus_id FK
        string name
        string code
        string description
        string email
        string phone
    }

    SERVICE {
        int id PK
        int department_id FK
        int building_id FK
        string name
        string description
        string category
        string email
        string phone
        string website
    }

    STAFF_MEMBER {
        int id PK
        int department_id FK
        string first_name
        string last_name
        string position
        string email
        string phone
    }

    CONTACT {
        int id PK
        int service_id FK
        string type
        string value
        string description
    }

    SCHEDULE {
        int id PK
        int service_id FK
        string day_of_week
        string opening_time
        string closing_time
    }

    ROLE {
        int id PK
        string name
        string description
    }

    USER {
        int id PK
        int role_id FK
        string username
        string email
        string password_hash
    }
```

---

# 7. Main Entities

## 7.1 University

The `University` entity represents the university organization.

### Fields

| Field       | Type    | Description           |
| ----------- | ------- | --------------------- |
| id          | Integer | Unique identifier     |
| name        | String  | University name       |
| description | String  | General description   |
| website     | String  | Official website      |
| email       | String  | General contact email |
| phone       | String  | General contact phone |

### Relationships

A university can have multiple campuses.

```text
University 1 ─────── N Campus
```

---

# 8. Campus

A `Campus` represents a physical university campus.

### Fields

| Field         | Type    | Description        |
| ------------- | ------- | ------------------ |
| id            | Integer | Unique identifier  |
| university_id | Integer | Related university |
| name          | String  | Campus name        |
| address       | String  | Street address     |
| city          | String  | City               |
| state         | String  | State              |
| postal_code   | String  | Postal code        |
| phone         | String  | Campus phone       |

### Relationship

```text
University 1 ─────── N Campus
```

One university can have many campuses.

---

# 9. Building

A `Building` represents a physical building located inside a campus.

### Fields

| Field       | Type    | Description          |
| ----------- | ------- | -------------------- |
| id          | Integer | Unique identifier    |
| campus_id   | Integer | Related campus       |
| name        | String  | Building name        |
| code        | String  | Building code        |
| address     | String  | Building address     |
| description | String  | Building description |

### Relationship

```text
Campus 1 ─────── N Building
```

One campus can contain many buildings.

---

# 10. Department

A `Department` represents an academic or administrative department.

Examples:

- Student Services
- Psychology
- Nursing
- Social Services
- Admissions
- Financial Aid
- Academic Affairs

### Fields

| Field       | Type    | Description            |
| ----------- | ------- | ---------------------- |
| id          | Integer | Unique identifier      |
| campus_id   | Integer | Related campus         |
| name        | String  | Department name        |
| code        | String  | Department code        |
| description | String  | Department description |
| email       | String  | Department email       |
| phone       | String  | Department phone       |

### Relationship

```text
Campus 1 ─────── N Department
```

A campus can contain multiple departments.

---

# 11. Service

The `Service` entity represents a service offered by the university.

Examples:

- Psychological counseling
- Nursing services
- Social services
- Student support
- Academic advising
- Financial aid
- Disability services

### Fields

| Field         | Type    | Description                           |
| ------------- | ------- | ------------------------------------- |
| id            | Integer | Unique identifier                     |
| department_id | Integer | Department providing the service      |
| building_id   | Integer | Building where the service is located |
| name          | String  | Service name                          |
| description   | String  | Service description                   |
| category      | String  | Service category                      |
| email         | String  | Service email                         |
| phone         | String  | Service phone                         |
| website       | String  | Service website                       |

### Relationships

```text
Department 1 ─────── N Service

Building 1 ─────── N Service
```

A department can provide multiple services.

A building can host multiple services.

---

# 12. Staff Member

The `StaffMember` entity represents university personnel.

### Fields

| Field         | Type    | Description        |
| ------------- | ------- | ------------------ |
| id            | Integer | Unique identifier  |
| department_id | Integer | Related department |
| first_name    | String  | First name         |
| last_name     | String  | Last name          |
| position      | String  | Job position       |
| email         | String  | Email address      |
| phone         | String  | Phone number       |

### Relationship

```text
Department 1 ─────── N StaffMember
```

One department can have multiple staff members.

---

# 13. Contact

The `Contact` entity stores different ways of contacting a university service.

A service may have multiple contact methods.

### Fields

| Field       | Type    | Description            |
| ----------- | ------- | ---------------------- |
| id          | Integer | Unique identifier      |
| service_id  | Integer | Related service        |
| type        | String  | Contact type           |
| value       | String  | Contact value          |
| description | String  | Additional information |

### Contact Types

Examples:

```text
email
phone
website
social_media
emergency
```

### Relationship

```text
Service 1 ─────── N Contact
```

---

# 14. Schedule

The `Schedule` entity represents the operating hours of a service.

### Fields

| Field        | Type    | Description       |
| ------------ | ------- | ----------------- |
| id           | Integer | Unique identifier |
| service_id   | Integer | Related service   |
| day_of_week  | String  | Day of the week   |
| opening_time | Time    | Opening time      |
| closing_time | Time    | Closing time      |

### Relationship

```text
Service 1 ─────── N Schedule
```

A service can have different schedules for different days.

Example:

```text
Monday    08:00 - 17:00
Tuesday   08:00 - 17:00
Wednesday 08:00 - 17:00
Thursday  08:00 - 17:00
Friday    08:00 - 15:00
```

---

# 15. User

The `User` entity represents an authenticated API user.

Users can be introduced when authentication and authorization are implemented.

### Fields

| Field         | Type    | Description       |
| ------------- | ------- | ----------------- |
| id            | Integer | Unique identifier |
| role_id       | Integer | User role         |
| username      | String  | Username          |
| email         | String  | Email address     |
| password_hash | String  | Hashed password   |

Passwords must never be stored as plain text.

---

# 16. Role

The `Role` entity defines what permissions an authenticated user has.

### Fields

| Field       | Type    | Description       |
| ----------- | ------- | ----------------- |
| id          | Integer | Unique identifier |
| name        | String  | Role name         |
| description | String  | Role description  |

Possible roles:

```text
admin
staff
student
readonly
```

### Relationship

```text
Role 1 ─────── N User
```

One role can be assigned to multiple users.

---

# 17. Primary Entity

For the initial project proposal, the primary entity can be:

## Service

The `Service` entity is central to the original problem because users need structured information about university services and how to contact them.

### Primary Entity Fields

1. id
2. department_id
3. building_id
4. name
5. description
6. category
7. email
8. phone
9. website

The API can use the service as an entry point for discovering university resources.

---

# 18. Related Entity

The primary related entity is:

## Contact

A university service can have multiple contact methods.

```text
Service 1 ─────── N Contact
```

For example:

```text
Psychological Counseling
    │
    ├── Email
    ├── Phone
    └── Website
```

This represents a one-to-many relationship.

---

# 19. Database Relationships

The main relationships are:

```text
University 1 ─── N Campus

Campus 1 ─── N Building

Campus 1 ─── N Department

Department 1 ─── N StaffMember

Department 1 ─── N Service

Building 1 ─── N Service

Service 1 ─── N Contact

Service 1 ─── N Schedule

Role 1 ─── N User
```

Visual hierarchy:

```text
University
    │
    └── Campus
          │
          ├── Building
          │
          └── Department
                │
                ├── Staff Member
                │
                └── Service
                      │
                      ├── Contact
                      │
                      └── Schedule
```

---

# 20. Normalization

The database should avoid unnecessary duplication of information.

For example, department information should not be duplicated inside every service.

Instead:

```text
Department
    id
    name
    email
```

and:

```text
Service
    id
    department_id
    name
```

The `department_id` establishes the relationship.

This allows the department information to be maintained in one place.

---

# 21. API Design

The API will use REST principles.

Base URL:

```text
/api/v1
```

Example resources:

```text
/api/v1/universities
/api/v1/campuses
/api/v1/buildings
/api/v1/departments
/api/v1/services
/api/v1/staff
/api/v1/contacts
/api/v1/schedules
```

---

# 22. Example Endpoints

## Universities

```http
GET /api/v1/universities
GET /api/v1/universities/{id}
```

## Campuses

```http
GET /api/v1/campuses
GET /api/v1/campuses/{id}
```

## Departments

```http
GET /api/v1/departments
GET /api/v1/departments/{id}
```

## Services

```http
GET /api/v1/services
GET /api/v1/services/{id}
```

## Staff

```http
GET /api/v1/staff
GET /api/v1/staff/{id}
```

## Contacts

```http
GET /api/v1/contacts
GET /api/v1/contacts/{id}
```

## Schedules

```http
GET /api/v1/schedules
GET /api/v1/schedules/{id}
```

---

# 23. Filtering and Query Parameters

The API can support query parameters for searching and filtering resources.

Example:

```http
GET /api/v1/services?category=health
```

```http
GET /api/v1/services?campus_id=1
```

```http
GET /api/v1/services?department_id=2
```

```http
GET /api/v1/services?search=psychology
```

Query parameters should be used for filtering collections.

Path parameters should be used when identifying a specific resource.

Example:

```http
GET /api/v1/services/10
```

---

# 24. API Response Structure

Responses should use JSON.

Example:

```json
{
  "id": 1,
  "name": "Psychological Counseling",
  "description": "Mental health and counseling services for students.",
  "category": "health",
  "email": "counseling@university.edu",
  "phone": "+1-555-0100",
  "website": "https://university.edu/counseling"
}
```

---

# 25. HTTP Status Codes

The API will use standard HTTP status codes.

| Status | Meaning                            |
| ------ | ---------------------------------- |
| 200    | Successful request                 |
| 201    | Resource created                   |
| 204    | Successful request with no content |
| 400    | Bad request                        |
| 401    | Authentication required            |
| 403    | Insufficient permissions           |
| 404    | Resource not found                 |
| 422    | Validation error                   |
| 500    | Internal server error              |

---

# 26. Authentication and Authorization

Authentication and authorization are part of the planned backend architecture.

Authentication answers:

```text
"Who is this user?"
```

Authorization answers:

```text
"What is this user allowed to do?"
```

The API can use role-based authorization.

Example:

```text
Admin
 ├── Create resources
 ├── Update resources
 ├── Delete resources
 └── Read resources

Staff
 ├── Create resources
 ├── Update resources
 └── Read resources

Student
 └── Read resources
```

Authentication and authorization can be expanded as the project develops.

---

# 27. Validation

Incoming API data should be validated before being processed.

Pydantic schemas will be used to validate request and response data.

Example:

```text
Request
   │
   ▼
Pydantic Schema
   │
   ├── Valid ──────► Service Layer
   │
   └── Invalid ────► 422 Response
```

---

# 28. Database Constraints

The database should enforce data integrity.

Examples include:

- Primary keys
- Foreign keys
- Required fields
- Unique constraints
- Valid relationships

For example:

```text
Service.department_id
        │
        ▼
Department.id
```

A service should not reference a department that does not exist.

---

# 29. Data Integrity

The application should prevent invalid relationships.

Examples:

- A service must belong to an existing department.
- A building must belong to an existing campus.
- A department must belong to an existing campus.
- A contact must belong to an existing service.
- A schedule must belong to an existing service.
- A staff member must belong to an existing department.

---

# 30. Database Environment

PostgreSQL runs as a Docker service inside the development environment.

Example development connection:

```text
postgresql://devuser:devpassword@postgres:5432/devdb
```

The database is isolated from the host machine and is accessible through the Docker network.

---

# 31. Docker Architecture

The development environment contains separate services.

```text
Docker Compose
│
├── app
│   └── FastAPI development environment
│
├── postgres
│   └── PostgreSQL database
│
└── redis
    └── Redis service
```

The application communicates with PostgreSQL through the Docker network.

Redis is available as an infrastructure service for future functionality such as:

- Caching
- Background jobs
- Temporary data
- Rate limiting

---

# 32. API Versioning

The API will use versioned routes.

Example:

```text
/api/v1/services
```

Future versions can be introduced without immediately breaking existing clients.

Example:

```text
/api/v1/services
/api/v2/services
```

---

# 33. Security Considerations

The API should follow basic security principles.

### Passwords

Passwords must never be stored directly.

Only password hashes should be stored.

### Environment Variables

Sensitive configuration should be stored in environment variables.

Examples:

```text
DATABASE_URL
SECRET_KEY
JWT_SECRET
```

Secrets should not be committed to GitHub.

### Input Validation

All external input should be validated before processing.

### Authorization

Protected operations should verify the user's permissions.

---

# 34. Initial Scope

The first milestone focuses on establishing the backend foundation and read-only API functionality.

Initial functionality includes:

- FastAPI application
- PostgreSQL database
- Docker development environment
- Basic database models
- Pydantic schemas
- REST API routes
- Read-only endpoints
- HTTP status codes
- Basic validation
- API documentation
- GitHub workflow
- Automated CI

The first API resources will focus on university services and their related information.

---

# 35. Future Scope

Future versions may include:

- Authentication
- Authorization
- User management
- Admin endpoints
- CRUD operations
- Advanced filtering
- Pagination
- Search
- Caching with Redis
- Notifications
- Appointment management
- Analytics
- More university entities
- External API integrations

---

# 36. Out of Scope for the Initial Milestone

The following functionality is not part of the initial milestone:

- Frontend application
- Mobile application
- Complex appointment systems
- Payment processing
- Advanced analytics
- Production deployment
- External authentication providers
- Advanced notification systems

The project is focused on building a reliable backend API that can later be consumed by different applications.

---

# 37. Design Principles

The project follows these principles:

### Separation of Concerns

Each layer has a specific responsibility.

### Reusability

The API should be usable by different client applications.

### Scalability

The data model should allow additional university resources to be added later.

### Consistency

API responses and error handling should follow consistent patterns.

### Data Integrity

Relationships and constraints should prevent invalid data.

### Security

Authentication, authorization, validation, and secret management should be considered throughout the system.

---

# 38. Architecture Summary

University Health is designed as a backend-first university information platform.

The core architecture is:

```text
                    CLIENT APPLICATIONS
                           │
                           ▼
                     REST API
                           │
                           ▼
                       FastAPI
                           │
                           ▼
                    Service Layer
                           │
                           ▼
                   Repository Layer
                           │
                           ▼
                      PostgreSQL
```

The core data model is:

```text
University
    │
    └── Campus
          │
          ├── Building
          │
          └── Department
                │
                ├── Staff Member
                │
                └── Service
                      │
                      ├── Contact
                      └── Schedule
```

This structure provides a foundation for a comprehensive university API while keeping the initial implementation manageable and extensible.
