
class BibaValidator:
    """Validador de integridad basado en el modelo de seguridad de Biba."""

    @staticmethod
    def validate(user_integrity: int, required_integrity: int) -> None:
        """Valida que un usuario tenga el nivel de integridad requerido para realizar una acción."""

        if user_integrity < required_integrity:
            raise PermissionError("No Write Up")
