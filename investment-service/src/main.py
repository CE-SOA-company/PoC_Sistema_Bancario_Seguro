from fastapi import FastAPI
from sqlalchemy.exc import OperationalError
import time

from src.infrastructure.database import init_db
from src.presentation.routes import router as investment_router

# Instancia principal de la aplicación FastAPI para el servicio de inversiones.
app = FastAPI(title="SecureBankito Investment Service") 

# Agrega las rutas relacionadas con inversiones al enrutador principal de la aplicación.
app.include_router(investment_router)


@app.on_event("startup")
def startup_event() -> None:
    """
    Evento de inicio de la aplicación que intenta inicializar la base de datos.
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
    Endpoint de verificación de salud para confirmar que el servicio está funcionando correctamente.
    """
    return {"status": "ok", "service": "investment-service"}
