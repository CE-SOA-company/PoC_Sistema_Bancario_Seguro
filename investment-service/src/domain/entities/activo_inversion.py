from dataclasses import dataclass


@dataclass(frozen=True)
class ActivoInversion:
    id: str
    name: str
    classification_level: int
