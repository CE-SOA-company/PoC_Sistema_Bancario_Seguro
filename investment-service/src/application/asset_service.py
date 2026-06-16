from src.domain.entities.activo_inversion import ActivoInversion
from src.domain.services.bell_lapadula_validator import BellLaPadulaValidator
from src.infrastructure.repository import AssetRepository


class AssetService:
    def __init__(self, repository: AssetRepository) -> None:
        self._repository = repository

    def list_vip_assets(self, user_clearance_level: int) -> list[ActivoInversion]:
        required_clearance = 3
        BellLaPadulaValidator.validate(user_clearance_level, required_clearance)
        return self._repository.list_all()
