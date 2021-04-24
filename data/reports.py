import sqlalchemy

from .db_session import SqlAlchemyBase


class Reports(SqlAlchemyBase):
    __tablename__ = 'reports'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    fileid = sqlalchemy.Column(sqlalchemy.Integer)
    filename = sqlalchemy.Column(sqlalchemy.String)
    # unique=True
