from src.domain.entities.usuario import Usuario
from src.domain.services.token_service import TokenService
from src.infrastructure.jwt_provider import JwtProvider
from src.infrastructure.repository import UserRepository


class AuthService:
    """
    Servicio de autenticación que maneja el proceso de login y generación de tokens JWT.
    Utiliza un repositorio para autenticar a los usuarios y un servicio de token para construir el payload del JWT.
    """

    def __init__(self, repository: UserRepository, token_service: TokenService, jwt_provider: JwtProvider) -> None:
        """
        Inicializa el servicio de autenticación con los componentes necesarios.
        """
        self._repository = repository
        self._token_service = token_service
        self._jwt_provider = jwt_provider

    def login(self, username: str, password: str) -> str:
        """
        Autentica a un usuario utilizando su nombre de usuario y contraseña
        Retorna un token JWT si la autenticación es exitosa.
        """
        usuario = self._repository.authenticate(username=username, password=password)
        payload = self._token_service.build_payload(usuario)
        return self._jwt_provider.encode(payload)
