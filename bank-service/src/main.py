from fastapi import FastAPI
from sqlalchemy.exc import OperationalError
import time

from src.infrastructure.database import init_db
from src.presentation.routes import router as bank_router


app = FastAPI(title="SecureBankito Bank Service")
app.include_router(bank_router)

@app.on_event("startup")
def startup_event() -> None:
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
    return {"status": "ok", "service": "bank-service"}
