# Wykorzystujemy stabilną wersję slim dla oszczędności miejsca
FROM docker.io/library/python:3.11-slim

# Zapobiega tworzeniu plików .pyc i zapewnia natychmiastowe logi
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instalacja zależności systemowych (narzędzia sieciowe i sterowniki baz danych)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    iputils-ping \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Instalacja kluczowych bibliotek do Data Engineeringu
# Instalujemy je tutaj, aby nie musieć przebudowywać obrazu przy każdej zmianie skryptów
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
    pandas \
    polars \
    sqlalchemy \
    psycopg2-binary \
    kafka-python \
    elasticsearch \
    requests \
    python-dotenv

# Tworzymy strukturę folderów zgodną z Twoim Medallion Architecture
RUN mkdir -p /scripts /bronze /silver /gold /files_csv /files_json /docker_volume

# Ustawiamy PYTHONPATH, aby Python widział Twoje moduły
ENV PYTHONPATH=/scripts

# Nie kopiujemy kodu tutaj, ponieważ używasz wolumenów (Volumes) do pracy "na żywo"
# To pozwala na edycję skryptów na hoście bez przebudowywania obrazu

CMD ["tail", "-f", "/dev/null"]