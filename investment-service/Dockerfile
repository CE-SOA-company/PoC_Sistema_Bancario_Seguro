FROM python:3.12-slim

WORKDIR /app

COPY investment-service/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY investment-service/ ./

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
