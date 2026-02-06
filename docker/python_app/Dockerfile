# --- ETAP 1: Builder ---
FROM docker.io/library/python:3.11-slim AS builder

WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --upgrade pip
COPY ./docker/python_app/requirements.txt .
# Instalujemy paczki do folderu lokalnego
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# --- ETAP 2: Runtime ---
FROM docker.io/library/python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/scripts

WORKDIR /app

# Kopiujemy tylko zainstalowane paczki z poprzedniego etapu
COPY --from=builder /install /usr/local

# Instalujemy tylko niezbędne narzędzia do debugowania i biblioteki runtime
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    vim \
    nano \
    net-tools \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Struktura Medallion
RUN mkdir -p /scripts /bronze /silver /gold /files_csv /files_json

CMD ["tail", "-f", "/dev/null"]