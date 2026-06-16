from dataclasses import dataclass

from src.domain.entities.usuario import Usuario


@dataclass(frozen=True)
class SecurityTokenPayload:
    sub: str
    username: str
    clearance_level: int
    integrity_level: int


class TokenService:
    def build_payload(self, usuario: Usuario) -> SecurityTokenPayload:
        return SecurityTokenPayload(
            sub=usuario.id,
            username=usuario.username,
            clearance_level=int(usuario.clearance_level),
            integrity_level=int(usuario.integrity_level),
        )