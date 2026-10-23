# GitHub Copilot Instructions — University Health API

## Stack Tecnológico

- **Lenguaje:** Python 3.12
- **Framework Web:** FastAPI (rutas asíncronas con tipado estricto)
- **Validación / DTOs:** Pydantic v2
- **ORM / Base de Datos:** SQLAlchemy 2.0 (PostgreSQL)
- **Migraciones:** Alembic
- **Gestor de Paquetes:** uv

## Estructura del Backend

```text
backend/app/
├── main.py              # App FastAPI, CORS, handlers y routers
├── config.py            # Settings
├── database.py          # Base, engine, sesión y get_db
├── models.py            # Modelos SQLAlchemy
├── schemas.py           # DTOs Pydantic
├── security.py          # JWT, hash y get_current_user
├── errors.py            # Errores de negocio
├── routers/             # Capa HTTP
├── services/            # Lógica de negocio
└── repositories/        # Acceso a datos
```

## Convenciones

- **Capas:** `router → service → repository → model`.
  - El router no consulta la base de datos ni aplica reglas de negocio.
  - El service valida reglas y reutiliza repositorios.
  - El repository es el único que ejecuta consultas SQLAlchemy.
- **DTOs:** `XxxDTO` para respuestas, `XxxCreate` para creación y `XxxUpdate`
  para actualización. Todos con `ConfigDict(from_attributes=True)` cuando
  salen desde un modelo.
- **Errores de negocio:** usar `NotFoundError`, `ConflictError` y
  `ValidationError` de `app/errors.py`. `main.py` los convierte en HTTP 404,
  409 y 400.
- **Tipado:** tipado estricto en todas las firmas de funciones y dependencias
  (`Depends`).
- **Base de datos:** inyección de dependencias mediante `get_db` con sesiones
  transaccionales.
- **Nuevos recursos:** crear un archivo en cada capa
  (`routers/x.py`, `services/x.py`, `repositories/x.py`), agregar el modelo en
  `models.py`, los DTO en `schemas.py` y registrar el router en `main.py`.
