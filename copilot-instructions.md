cat << 'EOF' > .github/copilot-instructions.md

# GitHub Copilot Instructions — University Health API

## Stack Tecnológico

- **Lenguaje:** Python 3.12
- **Framework Web:** FastAPI (rutas asíncronas con tipado estricto)
- **Validación / Esquemas:** Pydantic v2
- **ORM / Base de Datos:** SQLAlchemy 2.0 (PostgreSQL)
- **Migraciones:** Alembic
- **Gestor de Paquetes:** uv

## Convenciones de Código y Arquitectura

- **Estructura por Capas:**
  - `app/api/v1/`: Endpoints REST y routers modulares.
  - `app/services/`: Lógica de negocio pura (desacoplada de dependencias web).
  - `app/models/`: Modelos declarativos de SQLAlchemy 2.0.
  - `app/schemas/`: Esquemas de entrada y salida con Pydantic v2.
  - `app/authentication/`: Generación/validación de JWT y hashing de contraseñas.
  - `app/authorization/`: Roles, claims y decoradores/guards de control de acceso.
- **Tipado:** Tipado estricto en todas las firmas de funciones y dependencias (`Depends`).
- **Base de datos:** Inyección de dependencias mediante `get_db` con manejo de sesiones transaccionales.
  EOF
