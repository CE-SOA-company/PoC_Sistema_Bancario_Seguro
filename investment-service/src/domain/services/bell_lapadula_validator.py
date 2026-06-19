class BellLaPadulaValidator:
    """
    Validador de seguridad basado en el modelo Bell-LaPadula para controlar el acceso a los activos de inversión VIP.
    """
    @staticmethod
    def validate(user_clearance: int, required_clearance: int) -> None:
        """
        Valida si el nivel de autorización del usuario cumple con el requisito para acceder a los activos de inversión VIP.
        """
        if user_clearance < required_clearance:
            raise PermissionError("No Read Up")
