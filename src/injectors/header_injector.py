from fastapi import Header, Response


def inject_response_headers(response: Response) -> None:
    """Inyecta cabeceras personalizadas en cada respuesta HTTP."""
    response.headers["X-App-Name"] = "talent_hub"
    response.headers["X-API-Version"] = "1.0"


def get_application_config() -> dict:
    """Retorna la configuración general de la aplicación."""
    return {
        "app_name": "talent_hub",
        "version": "1.0.0",
        "description": "API para gestión de miembros del equipo",
    }
