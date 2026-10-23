# Estructura del backend

El backend quedó con una estructura plana, similar a Express: tres carpetas
principales (`routers`, `services`, `repositories`) y los archivos base en la
raíz de `app/`.

```text
backend/
├── app/
│   ├── main.py              # Crea FastAPI, CORS y registra los routers
│   ├── config.py            # Configuración y variables de entorno
│   ├── database.py          # Engine, sesión y get_db
│   ├── models.py            # Todas las tablas SQLAlchemy
│   ├── schemas.py           # Todos los DTO de Pydantic
│   ├── security.py          # Hash, JWT y get_current_user
│   ├── errors.py            # Errores de negocio
│   │
│   ├── routers/             # CAPA 1: recibe HTTP
│   │   ├── auth.py
│   │   ├── health.py
│   │   ├── roles.py
│   │   ├── users.py
│   │   ├── services.py
│   │   ├── staff_members.py
│   │   └── schedules.py
│   │
│   ├── services/            # CAPA 2: reglas de negocio
│   │   ├── role.py
│   │   ├── user.py
│   │   ├── service.py
│   │   ├── staff_member.py
│   │   └── schedule.py
│   │
│   └── repositories/        # CAPA 3: acceso a la base de datos
│       ├── base.py
│       ├── role.py
│       ├── user.py
│       ├── service.py
│       ├── staff_member.py
│       └── schedule.py
│
├── alembic/                 # Migraciones
├── seeds/seed.sql           # Datos de prueba
├── pyproject.toml
└── uv.lock
```

## Cómo se conectan las tres capas

```text
Petición HTTP
     ↓
router     → valida el DTO y llama al service
     ↓
service    → aplica las reglas de negocio y llama al repository
     ↓
repository → consulta o modifica la base de datos
     ↓
models     → tablas de SQLAlchemy
```

## Ejemplo real: listar usuarios

1. El router recibe la petición:

```python
# app/routers/users.py
@router.get("/", response_model=list[UserDTO])
async def get_users(db: AsyncSession = Depends(get_db)):
    return await user_service.list_users(db)
```

2. El service aplica la lógica y llama al repository:

```python
# app/services/user.py
async def list_users(db: AsyncSession) -> list[User]:
    return await UserRepository(db).get_all()
```

3. El repository consulta la base de datos:

```python
# app/repositories/user.py
async def get_all(self) -> list[User]:
    result = await self.db.execute(select(User))
    return list(result.scalars().all())
```

## Rutas disponibles

| Recurso        | Prefijo                     |
| -------------- | --------------------------- |
| Health         | `/health` y `/api/v1/health` |
| Autenticación  | `/api/v1/auth`              |
| Roles          | `/api/v1/roles`             |
| Usuarios       | `/api/v1/users`             |
| Servicios      | `/api/v1/services`          |
| Personal       | `/api/v1/staff-members`     |
| Horarios       | `/api/v1/schedules`         |

Cada recurso (excepto health y auth) tiene:

```text
GET     /            Listar
GET     /{id}        Obtener uno
POST    /            Crear
PUT     /{id}        Actualizar
DELETE  /{id}        Eliminar
```
