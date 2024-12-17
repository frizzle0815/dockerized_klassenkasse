# Verwenden des offiziellen Python 3.10 Slim Images
FROM python:3.10-slim

# Arbeitsverzeichnis setzen
WORKDIR /app

# Systemabhängigkeiten installieren
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Anforderungen kopieren und installieren
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Projektdateien kopieren
COPY . .

# Skript zum Warten auf PostgreSQL hinzufügen
COPY wait-for-postgres.sh /wait-for-postgres.sh
RUN chmod +x /wait-for-postgres.sh

# Port freigeben
EXPOSE 5100

# Startbefehl: Warten auf PostgreSQL und dann die Anwendung starten
CMD ["/wait-for-postgres.sh", "db", "python", "run.py"]