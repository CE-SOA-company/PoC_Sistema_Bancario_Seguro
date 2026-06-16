# SecureBankito

Base del proyecto para la PoC de sistema bancario seguro con DDD, Biba y Bell-LaPadula.

## Estructura inicial

- `iam-service/`: identidad, acceso y emisión de tokens.
- `bank-service/`: cuentas, transacciones y validación de integridad.
- `investment-service/`: activos VIP y validación de confidencialidad.
- `k8s/`: manifiestos de Kubernetes para Minikube.
- `docker-compose.yml`: entorno local para desarrollo y pruebas.

## Siguiente paso

1. Completar el microservicio IAM.
2. Montar el core bancario con Biba.
3. Montar inversiones con Bell-LaPadula.
4. Añadir Docker y Kubernetes.

## Documentación

- [Arquitectura](docs/architecture.md)
- [Escenarios de defensa](docs/security-scenarios.md)
- [Ejecución local](docs/local-setup.md)

