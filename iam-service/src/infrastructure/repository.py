import hashlib

from sqlalchemy import select

from src.domain.entities.usuario import Usuario
from src.domain.value_objects.clearance_level import ClearanceLevel
from src.domain.value_objects.integrity_level import IntegrityLevel
from src.infrastructure.database import SessionLocal
from src.infrastructure.models import UserModel


class UserRepository:
    def authenticate(self, username: str, password: str) -> Usuario:
        with SessionLocal() as session:
            statement = select(UserModel).where(UserModel.username == username)
            usuario = session.scalars(statement).first()
        if usuario is None or hashlib.sha256(password.encode()).hexdigest() != usuario.password_hash:
            raise ValueError("Invalid credentials")
        return Usuario(
            id=str(usuario.id),
            username=usuario.username,
            password_hash=usuario.password_hash,
            clearance_level=ClearanceLevel(usuario.clearance_level),
            integrity_level=IntegrityLevel(usuario.integrity_level),
        )
