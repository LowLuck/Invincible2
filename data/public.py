import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Public(SqlAlchemyBase):
    __tablename__ = 'pubfiles'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    content = sqlalchemy.Column(sqlalchemy.String)
    key = sqlalchemy.Column(sqlalchemy.String, unique=True)
    # unique=True
    user = orm.relation('User')
