#!/bin/sh
# Генерируем SSH host keys если их нет
ssh-keygen -A

# Создаём .ssh директорию
mkdir -p /home/jenkins/.ssh
chmod 700 /home/jenkins/.ssh

# Используем переменную окружения для установки публичного ключа
if [ -n "$JENKINS_AGENT_SSH_PUBKEY" ]; then
    echo "$JENKINS_AGENT_SSH_PUBKEY" > /home/jenkins/.ssh/authorized_keys
elif [ -f /tmp/secrets/jenkins_agent_ssh_key.pub ]; then
    # Иначе копируем из файла, если он существует
    cp /tmp/secrets/jenkins_agent_ssh_key.pub /home/jenkins/.ssh/authorized_keys
fi

if [ -f /home/jenkins/.ssh/authorized_keys ]; then
    chmod 600 /home/jenkins/.ssh/authorized_keys
    chown -R jenkins:jenkins /home/jenkins/.ssh
fi

# Запускаем SSH демона
exec /usr/sbin/sshd -D