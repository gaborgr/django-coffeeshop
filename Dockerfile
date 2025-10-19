# Imagen base
FROM python:3.11-slim

# Configuración básica
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=coffeeproject.settings

# Ddirectorio de trabajo dentro del contenedor
WORKDIR /app/coffeeproject

# Copia los requirements y los instala
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r /app/requirements.txt

# Copia el resto del código del proyecto
COPY . /app

# Comando para recolectar los archivos estaticos y ejecutar el servidor
CMD ["sh", "-c", "python manage.py migrate --noinput && python manage.py collectstatic --noinput && gunicorn coffeeproject.wsgi:application --bind 0.0.0.0:${PORT:-8080}"]
