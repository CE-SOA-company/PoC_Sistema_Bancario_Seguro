import os
import hashlib

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./iam.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass


def init_db() -> None:
    from src.infrastructure.models import UserModel

    def seed_user(
        username: str,
        password: str,
        clearance_level: int,
        integrity_level: int,
    ) -> None:
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

    Base.metadata.create_all(bind=engine)
    with SessionLocal() as session:
        seed_user("admin", "admin123", 3, 3)
        seed_user("bronze", "bronze123", 1, 1)
        seed_user("plata", "plata123", 2, 2)
        session.commit()
