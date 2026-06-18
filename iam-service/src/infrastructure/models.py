from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.database import Base


class UserModel(Base):
    """
    Modelo de usuario para la base de datos.
     - id:              Identificador único del usuario.
     - username:        Nombre de usuario.
     - password_hash:   Hash de la contraseña del usuario.
     - clearance_level: Nivel de autorización del usuario (0-5).
     - integrity_level: Nivel de integridad del usuario (0-5).
    """
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    clearance_level: Mapped[int] = mapped_column(Integer, nullable=False)
    integrity_level: Mapped[int] = mapped_column(Integer, nullable=False)
