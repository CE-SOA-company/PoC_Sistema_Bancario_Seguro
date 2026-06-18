from dataclasses import dataclass

from src.domain.entities.usuario import Usuario


@dataclass(frozen=True)
class SecurityTokenPayload:
    """
    Value Object que representa el payload del JWT de seguridad. 
    Contiene solo la información necesaria para la autorización, extraída del Usuario.
    """
    sub: str
    username: str
    clearance_level: int
    integrity_level: int


class TokenService:
    """
    Servicio de dominio, centraliza la lógica de construcción del payload del token de seguridad a partir de un Usuario autenticado.
    Actua como intermediario entre el dominio (Usuario) y la infraestructura (JWT).
    """
    def build_payload(self, usuario: Usuario) -> SecurityTokenPayload:
        """
        Construye el payload del token de seguridad a partir de un Usuario autenticado.
        Extrae los niveles de seguridad desde el NivelSeguridad del Usuario, para que el JWT siempre refleje las etiquetas del dominio.
        """
        return SecurityTokenPayload(
            sub=usuario.id,
            username=usuario.credenciales.username,
            clearance_level=int(usuario.nivel_seguridad.clearance),
            integrity_level=int(usuario.nivel_seguridad.integrity),
        )
