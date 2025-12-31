FROM python:3.11-slim

# Instalacja zależności systemowych
RUN apt-get update && apt-get install -y vim && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Najpierw kopiujemy i instalujemy requirements (wykorzystanie cache)
COPY docker/api/requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt

# Kopiujemy kod źródłowy
COPY src/dataprojectv1 /app/dataprojectv1

# Kluczowe zmienne dla Flaska i Pythona
ENV PYTHONPATH=/app
ENV FLASK_APP=dataprojectv1.api.app.app.py

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0", "--debug"]
# CMD ["flask", "run", "--host=0.0.0.0"]
# CMD ["python", "app.py"]
