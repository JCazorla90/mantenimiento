#!/usr/bin/python3

import os
import subprocess
#import smtplib
import socket
import ssl
import datetime
import requests

#Variables para el correo electrónico
smtp_server = "smtp.example.com"
port = 587
sender_email = "alerts@example.com"
receiver_email = "admin@example.com"
password = "password"

#Comando para obtener las versiones de los paquetes instalados
get_versions = "dpkg-query -W --showformat='${Package} ${Version}\n'"

#Comando para buscar actualizaciones disponibles
check_updates = "apt-get update && apt-get upgrade -s"

#Ejecutar los comandos y almacenar la salida en variables
installed_packages = subprocess.run(get_versions, shell=True, stdout=subprocess.PIPE)
available_updates = subprocess.run(check_updates, shell=True, stdout=subprocess.PIPE)

#Comprobar si hay actualizaciones disponibles
if "0 upgraded, 0 newly installed" not in str(available_updates.stdout):
# Enviar un correo electrónico con la información
    message = "Hay actualizaciones disponibles en el servidor:\n\n"
    message += "Paquetes instalados:\n"
    message += str(installed_packages.stdout.decode("utf-8"))
    message += "\nActualizaciones disponibles:\n"
    message += str(available_updates.stdout.decode("utf-8"))
    context = ssl.create_default_context()
    #with smtplib.SMTP(smtp_server, port) as server:
    #    server.ehlo()
    #    server.starttls(context=context)
    #    server.ehlo()
    #    server.login(sender_email, password)
    #    server.sendmail(sender_email, receiver_email, message)

#Comprobar si hay vulnerabilidades en los paquetes instalados (Este paso requiere una integración con una fuente de información de CVEs confiable)
def check_cves(package, version):
# Consultar la API de MITRE para obtener información sobre las vulnerabilidades
    url = f"https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword={package}%20{version}"
    response = requests.get(url)
    if response.status_code != 200:
        return None
        cve_info = response.text

# Procesar la información y comprobar si hay vulnerabilidades
    if "No matches were found" in cve_info:
        return None
    return cve_info

#Procesar cada paquete instalado y comprobar si hay vulnerabilidades
    vulnerable_packages = []
    for package in str(installed_packages.stdout.decode("utf-8")).split("\n"):
        name, version = package.split(" ")
        cve_info = check_cves(name, version)
    if cve_info:
        vulnerable_packages.append(package + ": " + cve_info)

    if vulnerable_packages is not None:
        message = "Hay paquetes vulnerables en el servidor:\n\n"
        message += "\n".join(vulnerable_packages)
        #with smtplib.SMTP(smtp_server, port) as server:
        #    server.ehlo()
        #    server.starttls(context=context)
        #    server.ehlo()
        #    server.login(sender_email, password)
        #    server.sendmail(sender_email, receiver_email, message)
