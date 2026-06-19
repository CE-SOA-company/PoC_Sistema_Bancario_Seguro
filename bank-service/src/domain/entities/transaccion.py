from dataclasses import dataclass
from datetime import datetime
from src.domain.value_objects.dinero import Dinero


@dataclass(frozen=True)
class Transaccion:
    """Representa una transacción financiera en el sistema bancario."""

    id: str
    account_id: str
    amount: Dinero
    created_at: datetime
    actor_integrity_level: int
