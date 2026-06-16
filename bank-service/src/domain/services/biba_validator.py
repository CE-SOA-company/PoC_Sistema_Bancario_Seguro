class BibaValidator:
    @staticmethod
    def validate(user_integrity: int, required_integrity: int) -> None:
        if user_integrity < required_integrity:
            raise PermissionError("No Write Up")
