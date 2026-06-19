# SecureBankito

> **Estudiantes:** Meibel Ceciliano Picado · Carlos Contreras Luna · Byron Mata Fuentes · Ludwin Ramos Briceño

Proyecto para la PoC de sistema bancario seguro con DDD, Biba y Bell-LaPadula.

## Requisitos

- Python 3.12
- Docker Desktop o Docker Engine
- Minikube
- kubectl

## Estructura del Proyecto

- `iam-service/`: Identidad, acceso y emisión de tokens.
- `bank-service/`: Cuentas, transacciones y validación de integridad.
- `investment-service/`: Activos VIP y validación de confidencialidad.
- `k8s/`: Manifiestos de Kubernetes para Minikube.
- `docker-compose.yml`: Entorno local para desarrollo y pruebas.
- `docs`: Manual de API de los servicios y justificación de diseño.
- `Diagramas`: Diagramas de dominio y secuencia.

## Documentación

- [Justificación de Diseño.](docs/Justificación_de_Diseño.md)

# Manual de API RESTful

- [Manual de los endpoints expuestos en formato OpenAPI de Bank Service.](docs/OpenAPI_bank_service.json)

- [Manual de los endpoints expuestos en formato OpenAPI de IAM Service.](docs/OpenAPI_iam_service.json)

- [Manual de los endpoints expuestos en formato OpenAPI de Investment Service.](docs/OpenAPI_investment_service.json)

## Diagramas

### Diagrama de Secuencia de Seguridad
<img src="Diagramas/Diagramas Proyecto 3 - Diagrama de Secuencia de Seguridad.svg" alt="Diagrama de Secuencia de Seguridad" width="700px" />

### Diagrama Dominio A
<img src="Diagramas/Dominio A.svg" alt="Diagrama Dominio A" width="700px" />

### Diagrama Dominio B
<img src="Diagramas/Dominio B.svg" alt="Dominio B" width="700px" />

### Diagrama Dominio 
<img src="Diagramas/Dominio C.svg" alt="Dominio C" width="700px" />


