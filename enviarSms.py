import csv
import logging
import os
import time
import tkinter as tk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tkinter import messagebox

# Configura el registro de actividad
logging.basicConfig(level=logging.INFO)

# Lee los parámetros configurables
perfil = os.getenv('PERFIL_FIREFOX', 'C:\\Users\\raton\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\zbs5lj38.default-release')
ruta_csv = os.getenv('RUTA_CSV', 'C:\\Users\\raton\\Downloads\\data.csv')

options = webdriver.FirefoxOptions()
options.add_argument('-profile')
options.add_argument(perfil)

try:
    # Inicia el navegador con el perfil especificado
    driver = webdriver.Firefox(options=options)

    # Contador para los mensajes enviados
    contador = 0

    # Abre el archivo CSV
    with open(ruta_csv, 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        for row in reader:
            # Extrae el número de teléfono, el nombre y el mensaje
            numero = row[0]
            nombre = row[1]
            mensaje = row[2]

            # Si todos los campos están vacíos, termina el script
            if not numero and not nombre and not mensaje:
                break

            # Si alguno de los campos está vacío, ignora esta fila y pasa a la siguiente
            if not numero or not nombre or not mensaje:
                continue

            # Formatea el mensaje
            mensaje = f"CFE: Estimado usuario {nombre}, {mensaje}"

            # Navega a la página de Google SMS
            driver.get("https://messages.google.com/web/conversations/new")

            # Espera a que la página se cargue
            time.sleep(5)

            # Encuentra el elemento input y escribe el número de teléfono
            input_element = driver.find_element(By.CLASS_NAME, "input")
            input_element.send_keys(numero)

            # Presiona ENTER para enviar el número de teléfono
            input_element.send_keys(Keys.RETURN)

            # Espera a que el chat se cargue
            time.sleep(4)

            # Escribe el mensaje en el chat
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "textarea")))
            textarea_element = driver.find_element(By.TAG_NAME, "textarea")
            textarea_element.send_keys(mensaje)

            # Presiona ENTER para enviar el mensaje
            textarea_element.send_keys(Keys.RETURN)

            # Incrementa el contador
            contador += 1
            logging.info(f'Mensaje {contador} enviado a {numero}')

            # Espera un poco antes de enviar el próximo mensaje
            time.sleep(3)

except Exception as e:
    logging.error(f'Ocurrió un error: {e}')
finally:
    # Cierra el navegador
    driver.quit()

# Muestra un mensaje con el recuento de mensajes enviados
root = tk.Tk()
root.withdraw()
messagebox.showinfo("SMS Enviados", f"Completado , Se enviaron {contador} mensajes.")
