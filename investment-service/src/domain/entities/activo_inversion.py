from dataclasses import dataclass, field


# Constante de dominio: todos los activos VIP son clasificación ORO (nivel 3).
# Definida aquí para que el dominio sea la única fuente de verdad sobre este valor.
CLASIFICACION_VIP = 3


@dataclass(frozen=True)
class ActivoInversion:
    """
    Aggregate Root del dominio de Inversiones VIP. Cada activo es único e identificado por su 'id'.
    Regla de dominio crítica: La clasificación es siempre ORO (nivel 3) y está fijada.
    """
    id: str
    name: str
    classification_level: int = field(default=CLASIFICACION_VIP, init=False)
