FROM python:3.11-slim

WORKDIR /app

# system deps for psycopg2-binary
RUN apt-get update -y --fix-missing
RUN apt-get install -y build-essential libpq-dev gcc  --fix-missing

COPY ./requirements.txt /app/requirements.txt
RUN python -m pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY ./app /app/app

ENV PYTHONUNBUFFERED=1

# run uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
