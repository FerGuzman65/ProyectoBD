# Usar imagen base ligera y oficial de Python
FROM python:3.9-slim

# Evitar que Python escriba archivos .pyc y forzar logs inmediatos
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Establecer directorio de trabajo en el contenedor
WORKDIR /app

# Instalar dependencias del sistema necesarias para compilar ciertas librerías de ML
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivo de requerimientos e instalar dependencias
COPY requirements.txt /app/
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copiar el script de la pipeline y el modelo a la imagen
COPY pipeline.py /app/
# El modelo será copiado si existe localmente, o se puede montar un volumen
COPY modelo_rul.pkl /app/

# Comando por defecto al iniciar el contenedor
CMD ["python", "pipeline.py"]
