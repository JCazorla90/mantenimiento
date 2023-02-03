#!/bin/bash

# Directorio raíz para la búsqueda de archivos sh y python
ROOT_DIR="/path/to/script/files"

# Dirección de correo electrónico para enviar el informe
EMAIL_ADDRESS="you@example.com"

# Nombre del archivo de informe
REPORT_FILE="script_report.txt"

# Crear el archivo de informe
echo "Tipo de archivo | Nombre del archivo | Ruta | Usuario | Fecha de creación | Última ejecución | Sintaxis correcta" > $REPORT_FILE

# Buscar todos los archivos sh y python en el directorio raíz
for file in $(find $ROOT_DIR -name "*.sh" -o -name "*.py"); do
  # Obtener información sobre el archivo
  filetype=$(file "$file" | awk -F, '{print $1}')
  filename=$(basename "$file")
  filepath=$(dirname "$file")
  owner=$(ls -l "$file" | awk '{print $3}')
  created_date=$(stat "$file" | grep "Modify:" | awk '{print $2, $3}')
  last_execution=$(stat "$file" | grep "Access:" | awk '{print $2, $3}')

  # Verificar si el archivo tiene una sintaxis correcta
  if [ "${file##*.}" == "sh" ]; then
    syntax_check=$(bash -n "$file")
  elif [ "${file##*.}" == "py" ]; then
    syntax_check=$(python -m py_compile "$file")
  fi

  if [ $? -ne 0 ]; then
    syntax_status="FAILED"
  else
    syntax_status="PASSED"
  fi

  # Escribir información en el archivo de informe
  echo "$filetype | $filename | $filepath | $owner | $created_date | $last_execution | $syntax_status" >> $REPORT_FILE
done

# Enviar el archivo de informe por correo electrónico
mail -s "Informe de Scripts" $EMAIL_ADDRESS < $REPORT_FILE

# Mostrar un mensaje indicando que se ha enviado el informe por correo electrónico
echo "El informe de scripts se ha enviado por correo electrónico a $EMAIL_ADDRESS"
