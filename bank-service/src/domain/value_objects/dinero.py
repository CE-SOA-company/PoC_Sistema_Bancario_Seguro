from dataclasses import dataclass


@dataclass(frozen=True)
class Dinero:
    amount: float
    currency: str = "USD"

    def __post_init__(self) -> None:
        if self.amount <= 0:
            raise ValueError("amount must be positive")
