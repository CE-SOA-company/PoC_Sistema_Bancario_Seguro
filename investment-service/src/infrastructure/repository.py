from sqlalchemy import select

from src.domain.entities.activo_inversion import ActivoInversion
from src.infrastructure.database import SessionLocal
from src.infrastructure.models import AssetModel


class AssetRepository:
    def list_all(self) -> list[ActivoInversion]:
        with SessionLocal() as session:
            statement = select(AssetModel)
            records = session.scalars(statement).all()
        return [
            ActivoInversion(id=record.asset_id, name=record.name, classification_level=record.classification_level)
            for record in records
        ]
