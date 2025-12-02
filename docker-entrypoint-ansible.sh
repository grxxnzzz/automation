#!/bin/bash
set -e

# Создаём директорию для SSH ключей
mkdir -p /home/ansible/.ssh
chmod 700 /home/ansible/.ssh

# Копируем SSH ключ для подключения к test-server
if [ -f /tmp/secrets/ansible_to_testserver_key ]; then
    cp /tmp/secrets/ansible_to_testserver_key /home/ansible/.ssh/id_rsa
    chmod 600 /home/ansible/.ssh/id_rsa
    chown ansible:ansible /home/ansible/.ssh/id_rsa 2>/dev/null || true
fi

# Бесконечный цикл чтобы контейнер не завершался
echo "Ansible agent started. Waiting for commands..."
tail -f /dev/null