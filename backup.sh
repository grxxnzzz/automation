#!/bin/bash
if [ -z "$1" ]; then
    echo "Error: Source directory not specified."
    exit 1
fi
if [ ! -d "$1" ]; then
    echo "Error: Source directory '$1' does not exist."
    exit 1
fi
BACKUP_DIR=${2:-/backup}
if [ ! -d "$BACKUP_DIR" ]; then
    mkdir -p "$BACKUP_DIR" || {
        echo "Error: Cannot create backup directory '$BACKUP_DIR'."
        exit 1
    }
fi
DATE=$(date +%Y%m%d_%H%M%S)
tar -czf "$BACKUP_DIR/backup_$DATE.tar.gz" "$1" || {
    echo "Error: Failed to create backup."
    exit 1
}
echo "Backup created successfully: $BACKUP_DIR/backup_$DATE.tar.gz"
