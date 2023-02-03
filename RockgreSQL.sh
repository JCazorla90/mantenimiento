#!/bin/bash

# Antes de empezar debes de tener PostgreSQL instalado y configurado en ambos servidores

# Configurar variables
OLD_HOST="centos_server_ip_address"
OLD_DB="old_database_name"
NEW_HOST="rocky_server_ip_address"
NEW_DB="new_database_name"
BACKUP_DIR="/path/to/backup/directory"

# Hacer una copia de seguridad de la base de datos en el servidor antiguo
pg_dump -F t -h $OLD_HOST -U postgres -f $BACKUP_DIR/$OLD_DB.tar $OLD_DB

# Copiar la copia de seguridad a Rocky Linux
scp $BACKUP_DIR/$OLD_DB.tar root@$NEW_HOST:$BACKUP_DIR/

# Conectarse a Rocky Linux y restaurar la base de datos
ssh root@$NEW_HOST << EOF
  pg_restore -C -h localhost -U postgres -d $NEW_DB $BACKUP_DIR/$OLD_DB.tar
  exit
EOF

# Optimizar la base de datos nueva
ssh root@$NEW_HOST << EOF
  psql -U postgres -c "VACUUM ANALYZE $NEW_DB"
  exit
EOF

# Verificar la integridad de la base de datos nueva
ssh root@$NEW_HOST << EOF
  psql -U postgres -c "SELECT * FROM pg_stat_activity WHERE datname='$NEW_DB'"
  exit
EOF
