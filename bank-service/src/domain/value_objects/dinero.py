from dataclasses import dataclass

@dataclass(frozen=True)
class Dinero:
    """Value object que representa una cantidad monetaria y su moneda."""

    amount: float
    currency: str = "USD"

    def __post_init__(self) -> None:
        """Valida que el monto sea positivo."""

        if self.amount <= 0:
            raise ValueError("amount must be positive")
