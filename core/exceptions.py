from typing import Any


class AppException(Exception):
    def __init__(self, status_code: int, message: str, error_code: str = "GENERIC"):
        self.status_code = status_code
        self.message = message
        self.error_code = error_code
        super().__init__(message)


class DuplicateRecord(AppException):
    def __init__(self, field: str):
        super().__init__(409, f"Ya existe un registro con ese {field}", "DUPLICATE_ENTRY")


class RecordNotFound(AppException):
    def __init__(self, entity: str, identifier: Any):
        super().__init__(404, f"{entity} '{identifier}' no fue encontrado", "NOT_FOUND")


class EmptyPayload(AppException):
    def __init__(self):
        super().__init__(422, "El cuerpo de la petición está vacío", "EMPTY_BODY")
