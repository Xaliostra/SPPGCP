FROM python:3.9
WORKDIR /app

# Копируем зависимости и устанавливаем их
COPY requirements.txt .
RUN pip install -r requirements.txt

# Копируем остальные файлы (включая index.html и app.py)
COPY . .

# Указываем Flask приложение
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=8080

# Открываем порт
EXPOSE 8080

# Запускаем Flask сервер
CMD ["flask", "run"]
