import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./investment.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass


def init_db() -> None:
    from src.infrastructure.models import AssetModel

    Base.metadata.create_all(bind=engine)
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
