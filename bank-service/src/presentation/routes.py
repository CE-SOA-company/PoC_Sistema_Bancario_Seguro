from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, ConfigDict, Field

from src.application.transfer_service import ProcesadorTransferencias
from src.infrastructure.repository import AccountRepository, TransactionRepository
from src.infrastructure.security import decode_access_token


router = APIRouter(prefix="/bank", tags=["bank"])
_procesador = ProcesadorTransferencias(AccountRepository(), TransactionRepository())
_bearer_scheme = HTTPBearer(auto_error=True)


class DepositRequest(BaseModel):
    """Modelo de solicitud para depositar en una cuenta bancaria."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "account_id": "gold-001",
                "amount": 50.0,
            }
        }
    )
    account_id: str = Field(description="Identificador de la cuenta", examples=["gold-001"])
    amount: float = Field(gt=0, description="Monto a depositar", examples=[50.0])

class DepositResponse(BaseModel):
    """Modelo de respuesta para la operación de depósito."""

    transaction_id: str = Field(description="Identificador único de la transacción")
    account_id: str = Field(description="Cuenta afectada")
    amount: float = Field(description="Monto depositado")
    actor_integrity_level: int = Field(description="Integridad usada en la validación Biba")

# Modelo de endpoint para depositar en una cuenta bancaria
@router.post(
    "/deposit",
    response_model=DepositResponse,
    summary="Depositar en cuenta",
    description=(
        "Lee integrity_level desde el JWT Bearer token y aplica Biba — No Write Up "
        "dentro del Aggregate Root CuentaBancaria: un proceso con integridad inferior "
        "a la requerida por la cuenta recibe 403 Forbidden."
    ),
)
# Endpoint para depositar en una cuenta bancaria
def deposit(
    payload: DepositRequest,
    credentials: HTTPAuthorizationCredentials = Depends(_bearer_scheme)
) -> DepositResponse:
    try:
        # Se decodifica el token de acceso para obtener la información del usuario, incluyendo el nivel de integridad
        claims = decode_access_token(credentials.credentials)
        
        # Se llama al método de depósito del procesador de transferencias, pasando el nivel de integridad del actor para aplicar la política de seguridad Biba  
        transaction = _procesador.deposit(
            account_id=payload.account_id,
            amount=payload.amount,
            actor_integrity_level=int(claims["integrity_level"]),
        )
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    return DepositResponse(
        transaction_id=transaction.id,
        account_id=transaction.account_id,
        amount=transaction.amount.amount,
        actor_integrity_level=transaction.actor_integrity_level,
    )
