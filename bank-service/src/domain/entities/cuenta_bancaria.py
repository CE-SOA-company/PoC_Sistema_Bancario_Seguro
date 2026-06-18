from dataclasses import dataclass, field

from src.domain.value_objects.dinero import Dinero
from src.domain.value_objects.integrity_level import IntegrityLevel


@dataclass
class CuentaBancaria:
    """
    Aggregate Root del dominio bancario.

    Es una Entity (y Aggregate Root) porque tiene identidad propia: cada
    cuenta es única, identificada por su 'id', con un ciclo de vida y un
    historial de transacciones propios.

    Responsabilidad de seguridad: el Aggregate Root protege su propio
    invariante de integridad (Biba — No Write Up). Ningún servicio externo
    puede depositar o retirar sin pasar por estos métodos, que validan la
    regla antes de mutar el estado. Esto garantiza que la regla de negocio
    no pueda ser omitida desde ninguna capa superior.
    """

    id: str
    owner_id: str
    balance: Dinero
    required_integrity_level: IntegrityLevel

    def deposit(self, amount: Dinero, actor_integrity: IntegrityLevel) -> None:
        """
        Aplica Biba — No Write Up antes de acreditar el monto.
        Lanza PermissionError si el actor no tiene integridad suficiente.
        """
        self._enforce_biba(actor_integrity, operation="depósito")
        self.balance = Dinero(self.balance.amount + amount.amount, self.balance.currency)

    def withdraw(self, amount: Dinero, actor_integrity: IntegrityLevel) -> None:
        """
        Aplica Biba — No Write Up antes de debitar el monto.
        Lanza PermissionError si el actor no tiene integridad suficiente.
        """
        self._enforce_biba(actor_integrity, operation="retiro")
        if amount.amount > self.balance.amount:
            raise ValueError("Fondos insuficientes")
        self.balance = Dinero(self.balance.amount - amount.amount, self.balance.currency)

    def _enforce_biba(self, actor_integrity: IntegrityLevel, operation: str) -> None:
        """
        Regla de integridad Biba — No Write Up:
        Un proceso con integridad inferior a la requerida por la cuenta
        no puede modificarla, para evitar corrupción de datos de alto valor.
        """
        if actor_integrity < self.required_integrity_level:
            raise PermissionError(
                f"Biba — No Write Up: integridad '{actor_integrity.name}' "
                f"insuficiente para {operation} en cuenta con nivel requerido "
                f"'{self.required_integrity_level.name}'."
            )
