from datetime import datetime, timezone
from uuid import uuid4

from src.domain.entities.transaccion import Transaccion
from src.domain.value_objects.dinero import Dinero
from src.domain.value_objects.integrity_level import IntegrityLevel
from src.infrastructure.repository import AccountRepository, TransactionRepository


class ProcesadorTransferencias:
    """
    Domain Service del Core Bancario.

    Orquesta el flujo de una transferencia: recupera la cuenta, delega la
    validación Biba al Aggregate Root (CuentaBancaria), persiste la
    transacción y actualiza el saldo.

    La validación de integridad NO ocurre aquí — ocurre dentro de
    CuentaBancaria.deposit(), que es quien protege sus propios invariantes.
    Este servicio solo coordina.
    """

    def __init__(self, account_repository: AccountRepository, transaction_repository: TransactionRepository) -> None:
        self._account_repository = account_repository
        self._transaction_repository = transaction_repository

    def deposit(self,account_id: str, amount: float, actor_integrity_level: int) -> Transaccion:
        """Realiza un depósito en la cuenta especificada, respetando la regla Biba No Write Up."""

        account = self._account_repository.get_by_id(account_id)
        money = Dinero(amount)
        actor_integrity = IntegrityLevel(actor_integrity_level)
        
        # La regla Biba No Write Up se valida dentro del Aggregate Root (CuentaBancaria).
        # Si el actor no tiene integridad suficiente, lanza PermissionError.
        account.deposit(money, actor_integrity) # Aquí se valida la regla Biba

        # Se crea y persiste la transacción después de modificar el estado de la cuenta, para garantizar consistencia
        transaction = Transaccion(
            id=str(uuid4()),
            account_id=account.id,
            amount=money,
            created_at=datetime.now(timezone.utc),
            actor_integrity_level=actor_integrity_level,
        )
        # Se persiste la transacción y luego se actualiza la cuenta
        self._transaction_repository.save(transaction)
        self._account_repository.save(account)
        return transaction
