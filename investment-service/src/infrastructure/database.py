import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# Configuración de la base de datos
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./investment.db")

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
    Inicializa la base de datos creando las tablas necesarias y agregando datos de ejemplo para los activos de inversión VIP.
    """
    from src.infrastructure.models import AssetModel

    # Crea las tablas en la base de datos
    Base.metadata.create_all(bind=engine)

    # Agrega datos de ejemplo para los activos de inversión VIP si no existen.
    with SessionLocal() as session:
        exists = session.query(AssetModel).filter(AssetModel.asset_id == "vip-001").first()
        if exists is None:
            session.add_all(
                [
                    AssetModel(asset_id="vip-001", name="Fondo Oro Privado", classification_level=3),
                    AssetModel(asset_id="vip-002", name="Portafolio Institucional Oro", classification_level=3),
                ]
            )
            session.commit()
