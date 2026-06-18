import os

import jwt
from fastapi import HTTPException
from jwt import PyJWTError

# Clave secreta que se utiliza para firmar y verificar los tokens JWT, es un valor predeterminado
JWT_SECRET = os.getenv("JWT_SECRET", "securebankito-dev-secret")

# Algoritmo de firma y validación de los tokens JWT ("HS256")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

def decode_access_token(token: str) -> dict[str, int | str]:

    # Si no se proporciona un token en la solicitud, se lanza una excepción HTTP 401
    if not token:
        raise HTTPException(status_code=401, detail="Missing access token")

    try:
        # Se intenta decodificar el token utilizando la clave secreta y el algoritmo especificados
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except PyJWTError as exc:
        # Si el token es inválido o ha expirado, se lanza una excepción HTTP 401.
        raise HTTPException(status_code=401, detail="Invalid or expired token") from exc
    try:
        # Se intenta extraer el nivel de integridad del payload del token
        integrity_level = int(payload["integrity_level"])
    except (KeyError, TypeError, ValueError) as exc:
        # si el nivel de integridad no se encuentra o no es un entero, se lanza una excepción HTTP 401.
        raise HTTPException(status_code=401, detail="Token missing integrity_level") from exc

    # Se retorna un diccionario con la información del usuario extraída del token
    return {
        "sub": str(payload.get("sub", "")),
        "username": str(payload.get("username", "")),
        "integrity_level": integrity_level,
    }
