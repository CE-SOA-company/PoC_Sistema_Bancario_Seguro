from datetime import datetime

from sqlalchemy import select

from src.domain.entities.cuenta_bancaria import CuentaBancaria
from src.domain.entities.transaccion import Transaccion
from src.domain.value_objects.dinero import Dinero
from src.infrastructure.database import SessionLocal
from src.infrastructure.models import AccountModel, TransactionModel


class AccountRepository:
    def get_by_id(self, account_id: str) -> CuentaBancaria:
        with SessionLocal() as session:
            statement = select(AccountModel).where(AccountModel.account_id == account_id)
            account = session.scalars(statement).first()
        if account is None:
            raise ValueError("Account not found")
        return CuentaBancaria(
            id=account.account_id,
            owner_id=account.owner_id,
            balance=Dinero(account.balance),
            required_integrity_level=account.required_integrity_level,
        )

    def save(self, account: CuentaBancaria) -> None:
        with SessionLocal() as session:
            statement = select(AccountModel).where(AccountModel.account_id == account.id)
            record = session.scalars(statement).first()
            if record is None:
                record = AccountModel(
                    account_id=account.id,
                    owner_id=account.owner_id,
                    balance=account.balance.amount,
                    required_integrity_level=account.required_integrity_level,
                )
                session.add(record)
            else:
                record.owner_id = account.owner_id
                record.balance = account.balance.amount
                record.required_integrity_level = account.required_integrity_level
            session.commit()


class TransactionRepository:
    def save(self, transaction: Transaccion) -> None:
        with SessionLocal() as session:
            session.add(
                TransactionModel(
                    transaction_id=transaction.id,
                    account_id=transaction.account_id,
                    amount=transaction.amount.amount,
                    actor_integrity_level=transaction.actor_integrity_level,
                    created_at=transaction.created_at.isoformat(),
                )
            )
            session.commit()
