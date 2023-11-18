# pylint: disable=invalid-name

wsgi_app = "rpi_remote_server.app:app"
bind = "localhost:8888"
workers = 4
proc_name = "rpi_remote_server"

access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" "%({name}i)s"'

syslog = True
syslog_addr = "unix:///dev/log#dgram"
