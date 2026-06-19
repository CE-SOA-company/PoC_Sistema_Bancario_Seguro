from dataclasses import dataclass

from src.domain.value_objects.credenciales import Credenciales
from src.domain.value_objects.nivel_seguridad import NivelSeguridad


@dataclass(frozen=True)
class Usuario:
    """
    Entidad raíz del dominio IAM.
    Tiene identidad propia (definida por un ID único), Agrupa dos Value Objects:
    - Credenciales: datos de autenticación (username + password_hash).
    - NivelSeguridad: las etiquetas de seguridad que el IAM emite en el JWT.
    """
    id: str
    credenciales: Credenciales
    nivel_seguridad: NivelSeguridad
