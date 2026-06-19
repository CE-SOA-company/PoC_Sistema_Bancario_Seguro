from fastapi import FastAPI
from sqlalchemy.exc import OperationalError
import time

from src.infrastructure.database import init_db
from src.presentation.routes import router as auth_router

# Inicializa la aplicación FastAPI
app = FastAPI(title="SecureBankito IAM Service")

# Incluye las rutas del módulo de autenticación
app.include_router(auth_router)


@app.on_event("startup")
def startup_event() -> None:
    """
    Intenta conectar a la base de datos y crear las tablas necesarias.
    Si la base de datos no está disponible, reintenta la conexión hasta 10 veces con un retraso de 2 segundos entre cada intento.
    """
    for attempt in range(10):
        try:
            init_db()
            return
        except OperationalError:
            if attempt == 9:
                raise
            time.sleep(2)


@app.get("/health")
def health_check() -> dict[str, str]:
    """
    Endpoint de salud para verificar que el servicio está funcionando correctamente.
    Retorna un mensaje de estado indicando que el servicio está operativo.
    """
    return {"status": "ok", "service": "iam-service"}
