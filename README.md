# Automatización del envío de mensajes con Google SMS

Este proyecto proporciona un script en Python para automatizar el envío de mensajes a través de Google SMS. El script lee un archivo CSV que contiene números de teléfono, nombres y mensajes, y luego envía estos mensajes a través de Google SMS utilizando Selenium.

## Requisitos

- Python 3.6 o superior
- Selenium
- Firefox
- Driver de Firefox (geckodriver)

## Dependencias

El proyecto requiere las siguientes dependencias, que se pueden instalar con `pip install -r requirements.txt`:

O con conda `pip install selenium`:

## Uso

1. Clona este repositorio en tu máquina local.
2. Instala las dependencias con `pip install -r requirements.txt`.
3. Asegúrate de tener Firefox y el driver de Firefox (geckodriver) instalados en tu sistema.
4. Actualiza la ruta al perfil de Firefox y la ruta al archivo CSV en el script `enviarSms.py`.
5. Ejecuta el script con `python enviarSms.py`.

## Funcionamiento

El script realiza las siguientes acciones:

1. Inicia Firefox con un perfil de usuario específico.
2. Abre un archivo CSV y lee cada fila.
3. Para cada fila, extrae el número de teléfono, el nombre y el mensaje.
4. Navega a la página de Google SMS.
5. Escribe el número de teléfono en el campo de entrada y presiona ENTER.
6. Escribe el mensaje en el chat y presiona ENTER.
7. Repite los pasos 4-6 para cada fila en el archivo CSV.
8. Al finalizar, muestra un mensaje con el recuento de mensajes enviados.

## Contribuciones

Las contribuciones a este proyecto son bienvenidas. Por favor, abre un issue para discutir la contribución antes de hacer un pull request.

## Licencia

Este proyecto está licenciado bajo los términos de la licencia MIT.
