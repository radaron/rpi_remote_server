# pylint: disable=invalid-name

wsgi_app = "rpi_remote_server.app:app"
bind = "0.0.0.0:8888"
workers = 1
proc_name = "rpi_remote_server"
worker_class = "eventlet"

accesslog = "-"
access_log_format = (
    '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" "%({name}i)s"'
)
