import os

bind = '0.0.0.0:{}'.format(os.environ['PORTA'])
user = 'inceres'
workers = int(os.environ.get('GUNICORN_WORKERS', 2))
timeout = 600
accesslog = '{}/access.log'.format(os.environ['LOG_DIR'])
errorlog = '{}/error.log'.format(os.environ['LOG_DIR'])
loglevel = 'debug'
capture_output = True
