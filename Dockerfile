FROM python:3.9
WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY index.html .
COPY . .

ENV PORT=8080
EXPOSE 8080

CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]
