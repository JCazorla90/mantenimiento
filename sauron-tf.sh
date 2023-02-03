#!/bin/bash

# Directorio raíz para la búsqueda de archivos Terraform
ROOT_DIR="/path/to/terraform/files"

# Dirección de correo electrónico para enviar el informe
EMAIL_ADDRESS="you@example.com"

# Nombre del archivo de informe
REPORT_FILE="terraform_report.txt"

# Crear el archivo de informe
echo "Nombre del archivo | Ruta | Usuario | Fecha de creación | Última ejecución | Sintaxis correcta" > $REPORT_FILE

# Buscar todos los archivos Terraform en el directorio raíz
for file in $(find $ROOT_DIR -name "*.tf"); do
  # Obtener información sobre el archivo
  filename=$(basename "$file")
  filepath=$(dirname "$file")
  owner=$(ls -l "$file" | awk '{print $3}')
  created_date=$(stat "$file" | grep "Modify:" | awk '{print $2, $3}')
  last_execution=$(stat "$file" | grep "Access:" | awk '{print $2, $3}')
  syntax_check=$(terraform fmt -check "$file")

  # Verificar si el archivo tiene una sintaxis correcta
  if [ $? -ne 0 ]; then
    syntax_status="FAILED"
  else
    syntax_status="PASSED"
  fi

  # Escribir información en el archivo de informe
  echo "$filename | $filepath | $owner | $created_date | $last_execution | $syntax_status" >> $REPORT_FILE
done

# Enviar el archivo de informe por correo electrónico
mail -s "Informe de Terraform" $EMAIL_ADDRESS < $REPORT_FILE

# Mostrar un mensaje indicando que se ha enviado el informe por correo electrónico
echo "El informe de Terraform se ha enviado por correo electrónico a $EMAIL_ADDRESS"
