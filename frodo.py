import os
import subprocess
import smtplib
import socket
import ssl
import datetime

# Variables para el correo electrónico
smtp_server = "smtp.example.com"
port = 587
sender_email = "alerts@example.com"
receiver_email = "admin@example.com"
password = "password"

# Comando para obtener las versiones de los paquetes instalados
get_versions = "dpkg-query -W --showformat='${Package} ${Version}\n'"

# Comando para buscar actualizaciones disponibles
check_updates = "apt-get update && apt-get upgrade -s"

# Ejecutar los comandos y almacenar la salida en variables
installed_packages = subprocess.run(get_versions, shell=True, stdout=subprocess.PIPE)
available_updates = subprocess.run(check_updates, shell=True, stdout=subprocess.PIPE)

# Comprobar si hay actualizaciones disponibles
if "0 upgraded, 0 newly installed" not in str(available_updates.stdout):
    # Enviar un correo electrónico con la información
    message = "Hay actualizaciones disponibles en el servidor:\n\n"
    message += "Paquetes instalados:\n"
    message += str(installed_packages.stdout.decode("utf-8"))
    message += "\nActualizaciones disponibles:\n"
    message += str(available_updates.stdout.decode("utf-8"))
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

# Comprobar si hay vulnerabilidades en los paquetes instalados
# (Este paso requiere una integración con una fuente de información de CVEs confiable)
# ...En construcción
