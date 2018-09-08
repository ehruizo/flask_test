# database
DB_HOST = '127.0.0.1'
DB_PORT = 5432
DB_DATABASE = 'bi'
DB_USER = 'biuser'
DB_PASSWORD = 1234
DB_SCHEMA = 'dv_rsa'

# esta configuración es usada por flask-sqlalchemy
SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}:{}/{}'.format(DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS = False

# flask configs
DEBUG = True
SECRET_KEY = 'THis is JUST Random gibberish!!@@@@@...++**}}[]'
SITE_PREFIX = ''  # '/api' o ''
