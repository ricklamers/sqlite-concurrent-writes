import time
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Log

engine = create_engine("sqlite:///log_database.sqlite3")
Session = sessionmaker(bind=engine)


def verify_log(start, end):
    """Verify logs"""
    session = Session()

    while True:
        all_logs = session.query(Log).order_by(Log.id).all()
        if len(all_logs) == end - start:
            return True
        time.sleep(5)

def main():
    """Entry point"""
    start = int(sys.argv[1])
    end = int(sys.argv[2])
    print(verify_log(start, end))

if __name__ == "__main__":
    main()
