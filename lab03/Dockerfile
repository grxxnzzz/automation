FROM python:3.11-slim

# Устанавливаем cron
RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/*

# Создаём рабочую директорию
WORKDIR /app

# Копируем файлы
COPY currency_exchange_rate.py /app/
COPY cronjob /etc/cron.d/lab03-cron
COPY entrypoint.sh /entrypoint.sh

# Даем права
RUN chmod 0644 /etc/cron.d/lab03-cron && chmod +x /entrypoint.sh

# Применяем cronjob
RUN crontab /etc/cron.d/lab03-cron

# Устанавливаем зависимости для Python-скрипта
RUN pip install requests

# Точка входа
ENTRYPOINT ["/entrypoint.sh"]