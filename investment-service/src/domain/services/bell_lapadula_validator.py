class BellLaPadulaValidator:
    @staticmethod
    def validate(user_clearance: int, required_clearance: int) -> None:
        if user_clearance < required_clearance:
            raise PermissionError("No Read Up")
