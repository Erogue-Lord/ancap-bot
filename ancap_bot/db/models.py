from sqlalchemy import TIMESTAMP, BigInteger, Column, Integer, Numeric
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, nullable=False)
    balance = Column(Numeric(10, 2), nullable=False, server_default="0.00")
    work = Column(TIMESTAMP)

    @classmethod
    def get_by_id(cls, id: int, session):
        return session.query(cls).filter_by(user_id=id).first()
