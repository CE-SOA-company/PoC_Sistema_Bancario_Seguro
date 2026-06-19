from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.database import Base


class AssetModel(Base):
    """
    Modelo de SQLAlchemy para representar um ativo financeiro na tabela "assets".
    """
    __tablename__ = "assets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    asset_id: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    classification_level: Mapped[int] = mapped_column(Integer, nullable=False)
