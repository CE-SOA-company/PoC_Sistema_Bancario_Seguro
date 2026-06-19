from datetime import datetime, timedelta, timezone

import jwt

from src.domain.services.token_service import SecurityTokenPayload


class JwtProvider:
    """
    Clase proveedora de JWT para emitir tokens con etiquetas de seguridad.
    """

    def __init__(self, secret_key: str = "securebankito-dev-secret", algorithm: str = "HS256") -> None:
        """
        Inicializa el proveedor de JWT.
        """
        self._secret_key = secret_key
        self._algorithm = algorithm

    def encode(self, payload: SecurityTokenPayload) -> str:
        """
        Codifica un payload de seguridad en un token JWT.
        Retorna el token JWT como string.
        """
        now = datetime.now(timezone.utc)
        claims = {
            "sub": payload.sub,
            "username": payload.username,
            "clearance_level": payload.clearance_level,
            "integrity_level": payload.integrity_level,
            "iat": now,
            "exp": now + timedelta(hours=1),
        }
        return jwt.encode(claims, self._secret_key, algorithm=self._algorithm)
