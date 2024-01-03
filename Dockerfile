FROM python:3.11

WORKDIR /app

ADD wait-for-it.sh /app
ADD gunicorn.conf.py /app
ADD rpi_remote_server /app/rpi_remote_server
ADD tools /app/tools
ADD data /app/data
ADD requirements.txt /app
ADD secret /app

RUN pip install --no-cache-dir --no-deps -r requirements.txt

EXPOSE 8080

CMD ["gunicorn"]