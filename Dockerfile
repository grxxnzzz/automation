FROM jenkins/ssh-agent:jdk11

# Установка PHP-CLI и зависимостей
RUN apt-get update && \
    apt-get install -y php-cli php-curl php-xml php-json php-mbstring && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Создание рабочей директории
RUN mkdir -p /home/jenkins/agent