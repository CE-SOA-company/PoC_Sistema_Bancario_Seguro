import os

import jwt
from fastapi import HTTPException
from jwt import PyJWTError


JWT_SECRET = os.getenv("JWT_SECRET", "securebankito-dev-secret")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")


def decode_access_token(token: str) -> dict[str, int | str]:
    """
    Decodifica y valida el JWT emitido por el IAM.
    """
    # Validación básica: el token debe estar presente.
    if not token:
        raise HTTPException(status_code=401, detail="Missing access token")
    # Decodifica el token usando la clave secreta y el algoritmo configurados.
    try: 
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except PyJWTError as exc:
        raise HTTPException(status_code=401, detail="Invalid or expired token") from exc
    # Validación adicional: el token debe contener el campo 'clearance_level' y debe ser un entero.
    try:
        clearance_level = int(payload["clearance_level"])
    except (KeyError, TypeError, ValueError) as exc:
        raise HTTPException(status_code=401, detail="Token missing clearance_level") from exc
    # Retorna un diccionario con la información relevante del token para su uso en la autorización.
    return {
        "sub": str(payload.get("sub", "")),
        "username": str(payload.get("username", "")),
        "clearance_level": clearance_level,
    }
