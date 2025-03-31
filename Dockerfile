FROM python:3.9
WORKDIR /app

COPY . .  # Скопирует ВСЕ файлы, включая index.html

RUN pip install -r requirements.txt

ENV PORT=8080
EXPOSE 8080

CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]

