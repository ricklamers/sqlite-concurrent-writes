import time

from sqlalchemy.exc import OperationalError
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

class Log(Base):
    __tablename__ = 'logs'

    id = Column(Integer, primary_key=True)
    text = Column(String)

def verify_log(start, end):
    engine = create_engine('sqlite:///log_database.sqlite3')
    try:
        Base.metadata.create_all(engine)
    except OperationalError:
        # Database already exists
        pass
    
    Session = sessionmaker(bind=engine)
    session = Session()

    while True:
        all_logs = session.query(Log).order_by(Log.id).all()
        if len(all_logs) == end-start and all(str(log.id) == log.text for log in all_logs):
            return True
        time.sleep(5)

if __name__ == "__main__":
    print(verify_log(1, 100))
