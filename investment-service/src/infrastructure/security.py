import os

import jwt
from fastapi import HTTPException
from jwt import PyJWTError


JWT_SECRET = os.getenv("JWT_SECRET", "securebankito-dev-secret")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")


def decode_access_token(token: str) -> dict[str, int | str]:
    if not token:
        raise HTTPException(status_code=401, detail="Missing access token")

    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except PyJWTError as exc:
        raise HTTPException(status_code=401, detail="Invalid or expired token") from exc

    try:
        clearance_level = int(payload["clearance_level"])
    except (KeyError, TypeError, ValueError) as exc:
        raise HTTPException(status_code=401, detail="Token missing clearance_level") from exc

    return {
        "sub": str(payload.get("sub", "")),
        "username": str(payload.get("username", "")),
        "clearance_level": clearance_level,
    }
