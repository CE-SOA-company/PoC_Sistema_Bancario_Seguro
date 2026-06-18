import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./bank.db") # URL de la base de datos

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

class Base(DeclarativeBase):
    pass

def init_db() -> None:
    """Inicializa la base de datos e inserta una cuenta de ejemplo, de tipo gold"""

    from src.infrastructure.models import AccountModel, TransactionModel

    Base.metadata.create_all(bind=engine)
    with SessionLocal() as session:
        exists = session.query(AccountModel).filter(AccountModel.account_id == "gold-001").first()
        if exists is None:
            session.add(
                AccountModel(
                    account_id="gold-001",
                    owner_id="1",
                    balance=1000.0,
                    required_integrity_level=3,
                )
            )
            session.commit()
