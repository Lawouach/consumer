FROM python:3.10.4-slim-buster

COPY app/main.py main.py
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --prefer-binary -r requirements.txt

ENV UVICORN_PORT 8080

ENTRYPOINT [ "uvicorn" ]
CMD ["--host", "0.0.0.0", "--forwarded-allow-ips", "*", "main:app" ]
