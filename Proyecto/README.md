# Comandos a ejecutar

`docker build -t actividad6.2 .  Construye la el contenedor con la imagen.`

`docker run --rm -v "C:\Maestría\Quinto-trimestre\Pruebas de software\Semana6\Proyecto\datos":/app/datos actividad6.2 Ejecuta el contenedor con la imagen y genera el resultado.`

`nota: utilice docker desktop para ejecutar el contenedor.`

`nota: para cambiar la ruta de cargar la información del contenedor, actualizar la ruta estática de docker run del segundo parámetro -v.`

`nota: para ejecutar el scripto con python, pylint o flake8 se debe actualizar el archivo Dockerfile de acuerdo al caso`

`# Comando para ejecutar python al iniciar`

`#CMD ["python", ".py"]`

`# Comando para ejecutar pylint al iniciar`

`CMD ["pylint", ".py"]`

`# Comando para ejecutar flake8 al iniciar`

`#CMD ["flake8", ".py"]`