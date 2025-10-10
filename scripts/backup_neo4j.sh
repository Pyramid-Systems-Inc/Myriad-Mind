#!/bin/bash
# Neo4j backup script for Myriad Cognitive Architecture

BACKUP_DIR="./backups/neo4j"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_NAME="myriad_backup_${TIMESTAMP}"

echo "Starting Neo4j backup: ${BACKUP_NAME}"

# Create backup directory if it doesn't exist
mkdir -p ${BACKUP_DIR}

# Create backup using neo4j-admin
docker exec neo4j neo4j-admin database backup \
  --to-path=/backups/${BACKUP_NAME} \
  neo4j

if [ $? -eq 0 ]; then
    echo "✅ Backup completed successfully: ${BACKUP_NAME}"
    
    # Compress backup
    cd ${BACKUP_DIR}
    tar -czf ${BACKUP_NAME}.tar.gz ${BACKUP_NAME}
    
    if [ $? -eq 0 ]; then
        # Remove uncompressed backup
        rm -rf ${BACKUP_NAME}
        
        # Keep only last 7 backups
        ls -t *.tar.gz | tail -n +8 | xargs -r rm
        
        echo "✅ Backup compressed and old backups cleaned"
        echo "📦 Backup location: ${BACKUP_DIR}/${BACKUP_NAME}.tar.gz"
    else
        echo "⚠️  Backup created but compression failed"
    fi
else
    echo "❌ Backup failed"
    exit 1
fi