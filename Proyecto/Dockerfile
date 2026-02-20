# Usar una imagen oficial ligera de Python
FROM python:3.9-slim

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

VOLUME /app/datos

# Instalar pylint
RUN pip install --no-cache-dir pandas pylint flake8

# Copiar el script al contenedor
COPY . .

# Comando para ejecutar el script
CMD ["python", "reserva_hotel.py"]
# Comando para ejecutar pylint al iniciar
#CMD ["pylint", "reserva_hotel.py"]
# Comando para ejecutar flake8 al iniciar
#CMD ["flake8", "reserva_hotel.py"]