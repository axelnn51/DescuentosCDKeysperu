FROM python:3.11-slim

# Evitar buffering en logs para verlos en tiempo real en Portainer
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV TZ=America/Lima

WORKDIR /app

# Instalar dependencias del sistema mínimas
RUN apt-get update && apt-get install -y --no-install-recommends \
    tzdata \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copiar requerimientos e instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente
COPY . .

# Crear carpeta de datos persistente
RUN mkdir -p /app/data

# Volumen persistente para la base de datos de deduplicación
VOLUME ["/app/data"]

# Comando de arranque por defecto: modo demonio continuo
CMD ["python", "spy.py", "--daemon"]
