from dataclasses import dataclass

from src.domain.value_objects.clearance_level import ClearanceLevel
from src.domain.value_objects.integrity_level import IntegrityLevel


@dataclass(frozen=True)
class NivelSeguridad:
    """
    Value Object que agrupa los dos criterios de seguridad de un sujeto como parte del dominio.
    Encapsula el clearance (confidencialidad) y la integridad (integridad).
    No tiene identidad propia, es inmutable (frozen=True) y se compara por valor
    """
    clearance: ClearanceLevel   # Criterio Bell-LaPadula (confidencialidad)
    integrity: IntegrityLevel   # Criterio Biba (integridad)

    def puede_leer(self, requerido: "NivelSeguridad") -> bool:
        """Bell-LaPadula — No Read Up: el clearance debe ser >= al requerido."""
        return self.clearance >= requerido.clearance

    def puede_escribir(self, requerido: "NivelSeguridad") -> bool:
        """Biba — No Write Up: la integridad debe ser >= a la requerida."""
        return self.integrity >= requerido.integrity

    def __str__(self) -> str:
        """Muestra el nivel de seguridad de forma legible."""
        return f"[Clearance={self.clearance.name}, Integrity={self.integrity.name}]"
