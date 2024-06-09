# Automatización del envío de mensajes con Google SMS

Este proyecto proporciona un script en Python para automatizar el envío de mensajes a través de Google SMS. El script lee un archivo CSV que contiene números de teléfono, nombres y mensajes, y luego envía estos mensajes a través de Google SMS utilizando Selenium.

## Requisitos

- Python 3.6 o superior
- Selenium
- Firefox
- Driver de Firefox (geckodriver)

## Pip list

Package                   Version
------------------------- -----------
anyio                     4.2.0
argon2-cffi               21.3.0
argon2-cffi-bindings      21.2.0
asttokens                 2.0.5
async-lru                 2.0.4
attrs                     23.2.0
Babel                     2.11.0
beautifulsoup4            4.12.2
bleach                    4.1.0
Brotli                    1.0.9
certifi                   2024.6.2
cffi                      1.16.0
charset-normalizer        2.0.4
colorama                  0.4.6
comm                      0.2.1
contourpy                 1.2.1
cryptography              42.0.8
cycler                    0.12.1
debugpy                   1.6.7
decorator                 5.1.1
defusedxml                0.7.1
exceptiongroup            1.2.0
executing                 0.8.3
fastjsonschema            2.16.2
fonttools                 4.53.0
h11                       0.14.0
idna                      3.7
ipykernel                 6.28.0
ipython                   8.20.0
jedi                      0.18.1
Jinja2                    3.1.4
json5                     0.9.6
jsonschema                4.19.2
jsonschema-specifications 2023.7.1
jupyter_client            8.6.0
jupyter_core              5.5.0
jupyter-events            0.8.0
jupyter-lsp               2.2.0
jupyter_server            2.10.0
jupyter_server_terminals  0.4.4
jupyterlab                4.0.11
jupyterlab-pygments       0.1.2
jupyterlab_server         2.25.1
kiwisolver                1.4.5
MarkupSafe                2.1.3
matplotlib                3.8.4
matplotlib-inline         0.1.6
mistune                   2.0.4
munkres                   1.1.4
nbclient                  0.8.0
nbconvert                 7.10.0
nbformat                  5.9.2
nest-asyncio              1.6.0
netifaces                 0.11.0
notebook                  7.0.8
notebook_shim             0.2.3
numpy                     1.26.4
outcome                   1.3.0.post0
overrides                 7.4.0
packaging                 23.2
pandocfilters             1.5.0
parso                     0.8.3
pillow                    10.3.0
pip                       24.0
platformdirs              3.10.0
prometheus-client         0.14.1
prompt-toolkit            3.0.43
psutil                    5.9.0
pure-eval                 0.2.2
pycparser                 2.21
Pygments                  2.15.1
pyparsing                 3.1.2
PySocks                   1.7.1
python-dateutil           2.9.0.post0
python-json-logger        2.0.7
pytz                      2024.1
pywin32                   305.1
pywinpty                  2.0.10
PyYAML                    6.0.1
pyzmq                     25.1.2
referencing               0.30.2
requests                  2.32.2
rfc3339-validator         0.1.4
rfc3986-validator         0.1.1
rpds-py                   0.10.6
scapy                     2.5.0
selenium                  4.21.0
Send2Trash                1.8.2
setuptools                69.5.1
six                       1.16.0
sniffio                   1.3.0
sortedcontainers          2.4.0
soupsieve                 2.5
stack-data                0.2.0
terminado                 0.17.1
tinycss2                  1.2.1
tk                        0.1.0
tomli                     2.0.1
tornado                   6.3.3
traitlets                 5.7.1
trio                      0.25.1
trio-websocket            0.11.1
typing_extensions         4.11.0
unicodedata2              15.1.0
urllib3                   2.2.1
wcwidth                   0.2.5
webencodings              0.5.1
websocket-client          1.8.0
wheel                     0.43.0
win-inet-pton             1.1.0
wsproto                   1.2.0

# Use conda for env

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
