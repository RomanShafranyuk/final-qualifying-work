import socket
import data_gen

def send_transaction(transaction):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))
    # transaction = data_gen.get_random_string(1024)
    client_socket.send(transaction.encode("utf-8"))
    client_socket.close()
