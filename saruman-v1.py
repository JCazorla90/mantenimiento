#!/usr/bin/env python3
import os
import subprocess
import socket

# Hostname del servidor
hostname = socket.gethostname()

# URL para descargar el paquete de instalación de Zabbix Agent
zabbix_agent_url = "https://repo.zabbix.com/zabbix/5.0/ubuntu/pool/main/z/zabbix-release/zabbix-release_5.0-1+focal_all.deb"

# Nombre del archivo descargado
zabbix_agent_file = "zabbix-release_5.0-1+focal_all.deb"

# Comando para descargar el paquete de instalación de Zabbix Agent
download_zabbix_agent = f"wget {zabbix_agent_url}"

# Comando para instalar el paquete de Zabbix Agent
install_zabbix_agent = "sudo apt-get install zabbix-agent"

# Comando para configurar el hostname en el archivo de configuración de Zabbix Agent
configure_zabbix_agent = f"sudo sed -i 's/Hostname=.*/Hostname={hostname}/' /etc/zabbix/zabbix_agentd.conf"

# URL para descargar el paquete de instalación de Wazuh Agent
wazuh_agent_url = "https://packages.wazuh.com/4.x/apt/pool/main/w/wazuh-agent/wazuh-agent_4.1.0-1_amd64.deb"

# Nombre del archivo descargado
wazuh_agent_file = "wazuh-agent_4.1.0-1_amd64.deb"

# Comando para descargar el paquete de instalación de Wazuh Agent
download_wazuh_agent = f"wget {wazuh_agent_url}"

# Comando para instalar el paquete de Wazuh Agent
install_wazuh_agent = "sudo apt-get install ./wazuh-agent_4.1.0-1_amd64.deb"

# Ejecutar los comandos para descargar e instalar los agentes
os.system(download_zabbix_agent)
os.system(f"sudo dpkg -i {zabbix_agent_file}")
os.system(install_zabbix_agent)
os.system(configure_zabbix_agent)
os.system(download_wazuh_agent)
os.system(install_wazuh_agent)

# Reiniciar los servicios de Zabbix y Wazuh Agent
os.system("sudo systemctl restart zabbix-agent")
os.system("sudo systemctl restart wazuh-agent")
