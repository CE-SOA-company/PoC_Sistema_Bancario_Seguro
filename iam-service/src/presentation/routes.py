from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict, Field

from src.application.auth_service import AuthService
from src.domain.services.token_service import TokenService
from src.infrastructure.jwt_provider import JwtProvider
from src.infrastructure.repository import UserRepository

# Ruta de autenticación para el IAM Service
router = APIRouter(prefix="/auth", tags=["auth"])

# Instancia del servicio de autenticación
_auth_service = AuthService(UserRepository(), TokenService(), JwtProvider())


class LoginRequest(BaseModel):
    """
    Esquema de solicitud para el endpoint de login.
    """
    
    # Configuración para incluir ejemplos en la documentación de OpenAPI
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "username": "admin",
                "password": "admin123",
            }
        }
    )

    # Campos de entrada para el login
    username: str = Field(description="Nombre de usuario registrado", examples=["admin"])
    password: str = Field(description="Contraseña del usuario", examples=["admin123"])


class LoginResponse(BaseModel):
    """
    Esquema de respuesta para el endpoint de login.
    """

    # Campos de salida después de un login exitoso
    access_token: str = Field(description="JWT con etiquetas de seguridad")
    token_type: str = Field(default="bearer", description="Tipo de token")


@router.post(
    "/login",
    response_model=LoginResponse,
    summary="Autenticar usuario",
    description="Emite un token JWT con clearance_level e integrity_level para los demás servicios.",
)
def login(payload: LoginRequest) -> LoginResponse:
    """
    Endpoint para autenticar a un usuario y emitir un token JWT con etiquetas de seguridad.
     - username: Nombre de usuario registrado.
     - password: Contraseña del usuario.
    """
    # Intenta autenticar al usuario. Genera un token JWT si las credenciales son correctas. Si no, devuelve un error 401.
    try:
        token = _auth_service.login(username=payload.username, password=payload.password)
    except ValueError as exc:
        raise HTTPException(status_code=401, detail=str(exc)) from exc
    return LoginResponse(access_token=token)