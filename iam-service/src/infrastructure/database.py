import os
import hashlib

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# Configuración de la base de datos
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./iam.db")

# Configuración de SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
)

# Creación de la sesión de base de datos
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    """
    Clase base para los modelos de SQLAlchemy.
    """
    pass


def init_db() -> None:
    """
    Inicializa la base de datos creando las tablas necesarias y agregando un usuario de ejemplo.
    """
    from src.infrastructure.models import UserModel

    def seed_user(
        username: str,
        password: str,
        clearance_level: int,
        integrity_level: int,
    ) -> None:
        """
        Agrega un usuario de ejemplo a la base de datos si no existe.
        """
        existing_user = session.query(UserModel).filter(UserModel.username == username).first()
        if existing_user is None:
            session.add(
                UserModel(
                    username=username,
                    password_hash=hashlib.sha256(password.encode()).hexdigest(),
                    clearance_level=clearance_level,
                    integrity_level=integrity_level,
                )
            )

    # Crea las tablas en la base de datos y agrega usuarios de ejemplo.
    Base.metadata.create_all(bind=engine)
    
    # Agrega usuarios de ejemplo con diferentes niveles de clearance e integrity.
    with SessionLocal() as session:
        seed_user("admin", "admin123", 3, 3)
        seed_user("bronze", "bronze123", 1, 1)
        seed_user("plata", "plata123", 2, 2)
        session.commit()
