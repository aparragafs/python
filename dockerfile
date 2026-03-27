FROM python:3.14-slim

WORKDIR /app

COPY prueba.py .

CMD ["python", "prueba.py"]