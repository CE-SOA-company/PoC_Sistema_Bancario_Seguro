from dataclasses import dataclass


@dataclass(frozen=True)
class Credenciales:
    """
    Value Object que representa las credenciales de autenticación de un Usuario.
    Encapsula el nombre de usuario y el hash de la contraseña
    No tiene identidad propia, es inmutable (frozen=True) y se compara por valor.
    """
    username: str
    password_hash: str
