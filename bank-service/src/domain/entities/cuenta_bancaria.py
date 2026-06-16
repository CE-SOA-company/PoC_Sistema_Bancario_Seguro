from dataclasses import dataclass

from src.domain.value_objects.dinero import Dinero


@dataclass
class CuentaBancaria:
    id: str
    owner_id: str
    balance: Dinero
    required_integrity_level: int

    def deposit(self, amount: Dinero) -> None:
        self.balance = Dinero(self.balance.amount + amount.amount, self.balance.currency)

