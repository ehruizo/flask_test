from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData


# flask configs
app = Flask(__name__)
app.config.from_object('settings')

# base de datos
meta = MetaData(schema=app.config['DB_SCHEMA'])
db = SQLAlchemy(app, metadata=meta)
