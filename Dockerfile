FROM python:3.12 AS builder
WORKDIR /app
COPY rpi_remote_server/ /app/rpi_remote_server/
COPY data/ /app/data/
COPY tools/ /app/tools/
COPY requirements.txt /app/requirements.txt
COPY gunicorn.conf.py /app/gunicorn.conf.py
RUN pip install --no-cache-dir --no-deps -r requirements.txt -t /app

FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /app/ /app/
EXPOSE 8888
EXPOSE 10000-20000
CMD ["python", "-m", "gunicorn"]
LABEL org.opencontainers.image.source=https://github.com/radaron/rpi_remote_server