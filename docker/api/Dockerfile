# Stage 1: Builder
FROM python:3.11-slim AS builder

# FROM python:3.11-slim

WORKDIR /app
COPY docker/api/requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Instalacja zależności systemowych
# RUN apt-get update && apt-get install -y vim && apt-get clean && rm -rf /var/lib/apt/lists/*
# WORKDIR /app
# # Najpierw kopiujemy i instalujemy requirements (wykorzystanie cache)
# COPY docker/api/requirements.txt /app/
# RUN pip install --no-cache-dir -r /app/requirements.txt

# Stage 2: Final
FROM python:3.11-slim

WORKDIR /app
# Kopiujemy tylko zainstalowane pakiety z buildera
COPY --from=builder /install /usr/local
# COPY src/dataprojectv1 /app/dataprojectv1
COPY . . 
# # Kopiujemy kod źródłowy
# COPY src/dataprojectv1 /app/dataprojectv1

# Kluczowe zmienne dla Flaska i Pythona
ENV PYTHONPATH=/app
# ENV FLASK_APP=dataprojectv1.api.app.app.py
ENV FLASK_APP=src.dataprojectv1.api.app.py

# Wyłączenie zapisu plików .pyc (oszczędność miejsca)
ENV PYTHONDONTWRITEBYTECODE=1

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0", "--debug"]
# CMD ["flask", "run", "--host=0.0.0.0"]
# CMD ["python", "app.py"]
