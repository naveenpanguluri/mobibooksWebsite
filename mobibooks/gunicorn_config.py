command = '/usr/local/bin/gunicorn'
pythonpath = '/home/www/wwwroot/mobibooks'
bind = '127.0.0.1:9001'
workers = 2
user = 'www'
debug = True
loglevel = 'debug'
#accesslog = '-'
#errorlog = '-'
pidfile='gunicorn.pid'
timeout = 900

