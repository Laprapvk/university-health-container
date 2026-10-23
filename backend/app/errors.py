class ServiceError(Exception):
    """Error base de la capa de servicios."""


class NotFoundError(ServiceError):
    """La entidad solicitada no existe."""


class ConflictError(ServiceError):
    """La operación entra en conflicto con datos existentes."""


class ValidationError(ServiceError):
    """Los datos de entrada no cumplen una regla de negocio."""
