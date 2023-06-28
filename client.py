import socket
import pickle

def store(obj) -> bool:
    """Store an object in the database"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = ('localhost', 10000)
    sock.connect(server_address)

    success = False
    try:
        # Send data
        data = pickle.dumps(obj)
        sock.sendall(data)

        # Wait for response
        response = sock.recv(4096)
        success = response.decode() == "OK"
    finally:
        sock.close()

    return success
