#!/bin/bash

# Guardar información de la sesión actual
HISTFILE=~/.bash_history

# Crear un archivo de log con la fecha y hora actual
LOG_FILE="session_log_$(date +%Y%m%d_%H%M%S).log"

# Capturar la IP del usuario
IP=$(echo $SSH_CONNECTION | awk '{print $1}')

# Guardar información de la sesión en el archivo de log
echo "Fecha y hora de inicio: $(date)" >> $LOG_FILE
echo "IP de conexión: $IP" >> $LOG_FILE
echo "Comandos ejecutados y sus respectivos PIDs:" >> $LOG_FILE

# Almacenar la información de los comandos y PIDs en tiempo real
PROMPT_COMMAND='{ echo "$(date +%Y-%m-%d\ %H:%M:%S) $(history 1 | awk "{print \$2\" \"\$3}") $(echo $!);" >> '$LOG_FILE'; }'

# Enviar el archivo de log al servidor a través de SFTP
scp $LOG_FILE user@server:/path/to/logs/
