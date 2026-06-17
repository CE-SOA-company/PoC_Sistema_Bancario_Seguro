from sqlalchemy import select

from src.domain.entities.activo_inversion import ActivoInversion
from src.infrastructure.database import SessionLocal
from src.infrastructure.models import AssetModel


class AssetRepository:
    """
    Repositorio para acceder a los modelos de activos de inversión.
    """
    def list_all(self) -> list[ActivoInversion]:
        """
        Lista todos los activos de inversión disponibles en la base de datos y los devuelve como una lista de objetos ActivoInversion.
        """
        with SessionLocal() as session:
            statement = select(AssetModel)
            records = session.scalars(statement).all()
        return [
            ActivoInversion(id=record.asset_id, name=record.name, classification_level=record.classification_level)
            for record in records
        ]
