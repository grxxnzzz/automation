#!/bin/sh
# Генерируем SSH host keys если их нет
ssh-keygen -A

# Если в /tmp/secrets есть pub ключ для ansible - добавляем его в authorized_keys
mkdir -p /home/ansible/.ssh
if [ -f /tmp/secrets/ansible_to_testserver_key.pub ]; then
    cat /tmp/secrets/ansible_to_testserver_key.pub > /home/ansible/.ssh/authorized_keys
    chown -R ansible:ansible /home/ansible/.ssh
    chmod 600 /home/ansible/.ssh/authorized_keys
fi

# Настраиваем SSH
sed -i 's/^#PermitRootLogin.*/PermitRootLogin no/' /etc/ssh/sshd_config
sed -i 's/^PermitRootLogin.*/PermitRootLogin no/' /etc/ssh/sshd_config

# Запускаем SSH
/usr/sbin/sshd

# Настраиваем Apache
echo "ServerName localhost" >> /etc/apache2/apache2.conf

# Запускаем Apache в foreground
exec apache2ctl -D FOREGROUND