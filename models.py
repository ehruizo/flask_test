from app import db


class Conversor(db.Model):
    __tablename__ = 'conversor'
    __table_args__ = {'autoload': True, 'autoload_with': db.engine}
