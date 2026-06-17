import hashlib

from sqlalchemy import select

from src.domain.entities.usuario import Usuario
from src.domain.value_objects.clearance_level import ClearanceLevel
from src.domain.value_objects.credenciales import Credenciales
from src.domain.value_objects.integrity_level import IntegrityLevel
from src.domain.value_objects.nivel_seguridad import NivelSeguridad
from src.infrastructure.database import SessionLocal
from src.infrastructure.models import UserModel


class UserRepository:
    """
    Repositorio para gestionar la persistencia de usuarios en la base de datos.
    Propociona métodos para autenticar un usuario y recuperar su información de seguridad.
    """
    def authenticate(self, username: str, password: str) -> Usuario:
        """Autentica a un usuario utilizando su nombre de usuario y contraseña."""
        
        # Consulta la base de datos para obtener el usuario por su nombre de usuario
        with SessionLocal() as session:
            statement = select(UserModel).where(UserModel.username == username)
            usuario = session.scalars(statement).first()

        # Verifica si el usuario existe y si la contraseña es correcta
        if usuario is None or hashlib.sha256(password.encode()).hexdigest() != usuario.password_hash:
            raise ValueError("Invalid credentials")

        # Converte el modelo de usuario a la entidad de dominio Usuario (ID, credenciales, nivel de seguridad)
        return Usuario(
            id=str(usuario.id),
            credenciales=Credenciales(
                username=usuario.username,
                password_hash=usuario.password_hash,
            ),
            nivel_seguridad=NivelSeguridad(
                clearance=ClearanceLevel(usuario.clearance_level),
                integrity=IntegrityLevel(usuario.integrity_level),
            ),
        )
