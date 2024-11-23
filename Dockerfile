FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir --trusted-host pypi.python.org -r requirements.txt

CMD ["python", "run.py", "--host=0.0.0.0"]