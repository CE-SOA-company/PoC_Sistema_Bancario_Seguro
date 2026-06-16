from datetime import datetime, timezone
from uuid import uuid4

from src.domain.entities.transaccion import Transaccion
from src.domain.services.biba_validator import BibaValidator
from src.domain.value_objects.dinero import Dinero
from src.infrastructure.repository import AccountRepository, TransactionRepository


class TransferService:
    def __init__(self, account_repository: AccountRepository, transaction_repository: TransactionRepository) -> None:
        self._account_repository = account_repository
        self._transaction_repository = transaction_repository

    def deposit(self, account_id: str, amount: float, actor_integrity_level: int) -> Transaccion:
        account = self._account_repository.get_by_id(account_id)
        BibaValidator.validate(actor_integrity_level, account.required_integrity_level)
        money = Dinero(amount)
        account.deposit(money)
        transaction = Transaccion(
            id=str(uuid4()),
            account_id=account.id,
            amount=money,
            created_at=datetime.now(timezone.utc),
            actor_integrity_level=actor_integrity_level,
        )
        self._transaction_repository.save(transaction)
        self._account_repository.save(account)
        return transaction
