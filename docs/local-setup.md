# Ejecución Local

## Requisitos

- Python 3.12
- Docker Desktop o Docker Engine
- Minikube
- kubectl

## Desarrollo local

1. Levanta los servicios con `docker compose up --build`.
2. IAM expone `http://localhost:8001`.
3. Bank expone `http://localhost:8002`.
4. Investment expone `http://localhost:8003`.

## Swagger / OpenAPI

1. IAM docs: `http://localhost:8001/docs`
2. Bank docs: `http://localhost:8002/docs`
3. Investment docs: `http://localhost:8003/docs`
4. OpenAPI JSON: `http://localhost:8001/openapi.json`, `http://localhost:8002/openapi.json`, `http://localhost:8003/openapi.json`

## Postman

1. Import `postman/SecureBankito.postman_collection.json`.
2. Import `postman/SecureBankito.postman_environment.json`.
3. Ejecuta primero `IAM > Login admin` para guardar `accessToken`.
4. Luego corre los casos de Bank e Investment.

## Kubernetes

1. Ejecuta `minikube start`.
2. Aplica los manifiestos de `k8s/`.
3. Verifica pods y services con `kubectl get pods` y `kubectl get services`.

## Migraciones

1. Entra a cada servicio, por ejemplo `iam-service`.
2. Ejecuta `alembic upgrade head` usando el `DATABASE_URL` del entorno.
3. Repite en `bank-service` e `investment-service`.

