FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir --trusted-host pypi.python.org -r requirements.txt

CMD ["gunicorn", "--bind", "0.0.0.0:80", "run:app"]