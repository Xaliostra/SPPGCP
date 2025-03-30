FROM python:3.9
WORKDIR /app

COPY requirements.txt .
COPY index.html
RUN pip install -r requirements.txt
COPY . .

CMD ["python", "app.py"]
