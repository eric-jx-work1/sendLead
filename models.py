from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    resume = Column(String)
    state = Column(Enum("PENDING", "REACHED_OUT", name="lead_state"), default="PENDING")
