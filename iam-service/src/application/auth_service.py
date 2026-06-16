from src.domain.entities.usuario import Usuario
from src.domain.services.token_service import TokenService
from src.infrastructure.jwt_provider import JwtProvider
from src.infrastructure.repository import UserRepository


class AuthService:
    def __init__(self, repository: UserRepository, token_service: TokenService, jwt_provider: JwtProvider) -> None:
        self._repository = repository
        self._token_service = token_service
        self._jwt_provider = jwt_provider

    def login(self, username: str, password: str) -> str:
        usuario = self._repository.authenticate(username=username, password=password)
        payload = self._token_service.build_payload(usuario)
        return self._jwt_provider.encode(payload)
