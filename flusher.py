import signal
import sys
import threading
import socketserver
import pickle

from pickle import UnpicklingError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError, OperationalError

from models import Base


engine = create_engine('sqlite:///log_database.sqlite3')
Session = sessionmaker(bind=engine)

# Create database if it doesn't exist
Base.metadata.create_all(engine)

lock = threading.Lock()

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        lock.acquire()

        session = Session()
        while True:
            # Receive the data in small chunks
            data = self.request.recv(4096)

            if not data:
                # Client closed connection
                break

            # Unpickle the received data
            try:
                entry = pickle.loads(data)
            except (UnpicklingError, ValueError, TypeError):
                self.request.sendall(b'ERROR')
                continue

            try:
                session.add(entry)
                session.commit()
                self.request.sendall(b'OK')
            except (IntegrityError, OperationalError) as error:
                print("ERROR:", error, type(error))
                self.request.sendall(b'ERROR')
                session.rollback()

        session.close()
        lock.release()


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

if __name__ == "__main__":
    HOST, PORT = "localhost", 10000

    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)

    def signal_handler(_sig, _frame):
        """Handle SIGINT signal"""
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    server.serve_forever()
