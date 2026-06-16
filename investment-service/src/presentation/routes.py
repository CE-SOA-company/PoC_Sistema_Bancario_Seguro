from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, Field

from src.application.asset_service import AssetService
from src.infrastructure.repository import AssetRepository
from src.infrastructure.security import decode_access_token


router = APIRouter(prefix="/investments", tags=["investments"])
_asset_service = AssetService(AssetRepository())
_bearer_scheme = HTTPBearer(auto_error=True)


class AssetResponse(BaseModel):
    id: str = Field(description="Identificador del activo VIP")
    name: str = Field(description="Nombre descriptivo del activo")
    classification_level: int = Field(description="Nivel de clasificación requerido")


@router.get(
    "/assets",
    response_model=list[AssetResponse],
    summary="Listar activos VIP",
    description="Lee clearance_level desde el JWT Bearer token y aplica Bell-LaPadula: un clearance inferior al requerido recibe 403 No Read Up.",
)
def list_assets(
    credentials: HTTPAuthorizationCredentials = Depends(_bearer_scheme),
) -> list[AssetResponse]:
    try:
        claims = decode_access_token(credentials.credentials)
        assets = _asset_service.list_vip_assets(user_clearance_level=int(claims["clearance_level"]))
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    return [
        AssetResponse(id=asset.id, name=asset.name, classification_level=asset.classification_level)
        for asset in assets
    ]