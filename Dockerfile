FROM python:3.8.10

WORKDIR /api/

COPY . .
RUN apt-get update \
    && apt-get install -y libpq-dev

RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /api/app/

CMD ["uvicorn", "main:app",  "--host", "0.0.0.0", "--port", "80"]