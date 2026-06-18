from sqlalchemy import select

from src.domain.entities.cuenta_bancaria import CuentaBancaria
from src.domain.entities.transaccion import Transaccion
from src.domain.value_objects.dinero import Dinero
from src.domain.value_objects.integrity_level import IntegrityLevel
from src.infrastructure.database import SessionLocal
from src.infrastructure.models import AccountModel, TransactionModel


class AccountRepository:
    """Repositorio para manejar la comunicación con la base de datos de cuentas bancarias."""

    def get_by_id(self, account_id: str) -> CuentaBancaria:
        """Obtiene una cuenta bancaria por su ID."""

        with SessionLocal() as session:
            statement = select(AccountModel).where(AccountModel.account_id == account_id)
            account = session.scalars(statement).first()

        if account is None:
            raise ValueError("Account not found")

        # Se convierte el registro de la base de datos a una entidad del dominio
        return CuentaBancaria(
            id=account.account_id,
            owner_id=account.owner_id,
            balance=Dinero(account.balance),
            # Se convierte el int de la BD al enum del dominio
            required_integrity_level=IntegrityLevel(account.required_integrity_level),
        )

    def save(self, account: CuentaBancaria) -> None:
        """Guarda o actualiza una cuenta bancaria en la base de datos."""

        with SessionLocal() as session:
            statement = select(AccountModel).where(AccountModel.account_id == account.id)
            record = session.scalars(statement).first()

            if record is None:
                # Se crea un nuevo registro si no existe
                record = AccountModel(
                    account_id=account.id,
                    owner_id=account.owner_id,
                    balance=account.balance.amount,
                    # Se convierte el valor del enum a int
                    required_integrity_level=int(account.required_integrity_level),
                )
                session.add(record)
            else:
                # Si el registro ya existe, se actualizan los campos
                record.owner_id = account.owner_id
                record.balance = account.balance.amount
                record.required_integrity_level = int(account.required_integrity_level)

            session.commit()


class TransactionRepository:
    """Repositorio para manejar la comunicación con la base de datos de transacciones."""

    def save(self, transaction: Transaccion) -> None:
        """Guarda una transacción en la base de datos."""
        
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
