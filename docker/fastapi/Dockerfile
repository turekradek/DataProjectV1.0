FROM python:3.11-slim
WORKDIR /app
COPY ./docker/fastapi/requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir fastapi uvicorn psycopg2-binary tabulate
# Kopiujemy resztę plików
COPY . .
CMD ["uvicorn", "src.dataprojectv1.fastapi.main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]