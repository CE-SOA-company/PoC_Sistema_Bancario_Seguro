from src.domain.entities.activo_inversion import ActivoInversion
from src.domain.services.bell_lapadula_validator import BellLaPadulaValidator
from src.infrastructure.repository import AssetRepository


class AssetService:
    """
    Servicio de aplicación para gestionar activos de inversión.
    """
    def __init__(self, repository: AssetRepository) -> None:
        """
        Inicializa el servicio de activos de inversión.
        """
        self._repository = repository

    def list_vip_assets(self, user_clearance_level: int) -> list[ActivoInversion]:
        """
        Lista los activos de inversión VIP disponibles para un usuario con un nivel de autorización específico.
        """
        required_clearance = 3
        BellLaPadulaValidator.validate(user_clearance_level, required_clearance)
        return self._repository.list_all()
