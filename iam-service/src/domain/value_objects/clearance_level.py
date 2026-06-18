from enum import IntEnum


class ClearanceLevel(IntEnum):
    """
    Representa los niveles de autorización de un usuario.
    """
    BRONCE = 1
    PLATA = 2
    ORO = 3
