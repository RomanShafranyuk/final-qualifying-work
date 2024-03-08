import socket
import hashlib
import json
import data_gen
import sys
import network
SERVER_ADDRESS = ('25.18.233.38',7001)
BLOCK_COUNT = 1000
BLOCK_SIZE = 1024
def send_transaction(count_transactions, transaction_size):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(SERVER_ADDRESS)
    print("Клиент подключился к серверу ")
    print("Начата генерация транзакций")
    transactions = data_gen.generate_block_data(count_transactions, transaction_size)
    for i in range(len(transactions)):
        signature = hashlib.sha256(transactions[i].encode("utf-8")).hexdigest()
        transactions[i] = (transactions[i], signature)
    print("Транзакции сформированы")
    message = json.dumps(transactions).encode("utf-8")
    message_size = sys.getsizeof(message)
    network.send_message(message, client_socket, message_size)
    client_socket.close()

send_transaction(BLOCK_COUNT,BLOCK_SIZE)