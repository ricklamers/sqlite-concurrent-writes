import os

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

# Get process id
pid = os.getpid()

class Log(Base):
    __tablename__ = 'logs'

    id = Column(Integer, primary_key=True)
    text = Column(String)

def write_log(start, end):
    engine = create_engine('sqlite:///log_database.sqlite3')
    try:
        Base.metadata.create_all(engine)
    except OperationalError:
        pass

    Session = sessionmaker(bind=engine)
    session = Session()

    for i in range(start, end):
        log = Log(id=i, text=str(i))
        print(f"Writing log {i} to database from PID {pid}", flush=True)
        session.add(log)

    session.commit()

if __name__ == "__main__":
    import sys
    start = int(sys.argv[1])
    end = int(sys.argv[2])
    write_log(start, end)
