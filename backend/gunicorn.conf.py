# pylint: disable=invalid-name

wsgi_app = "main:app"
bind = "0.0.0.0:8080"
workers = 4
proc_name = "rpi_central"

access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" "%({name}i)s"'

syslog = True
syslog_addr = "unix:///dev/log#dgram"
