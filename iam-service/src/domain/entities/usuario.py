from dataclasses import dataclass

from src.domain.value_objects.clearance_level import ClearanceLevel
from src.domain.value_objects.integrity_level import IntegrityLevel


@dataclass(frozen=True)
class Usuario:
    id: str
    username: str
    password_hash: str
    clearance_level: ClearanceLevel
    integrity_level: IntegrityLevel
