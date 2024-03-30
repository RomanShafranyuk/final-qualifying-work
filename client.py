import socket
import hashlib
import transactions_gen
import network
socket.setdefaulttimeout(2)
SERVER_ADDRESS = ('25.18.233.38',7001)
TRANSACTION_COUNT = 10000
TRANSACTION_SIZE = 1024

    

if __name__ == "__main__":
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(SERVER_ADDRESS)
    print("Клиент подключился к серверу ")
    print("Начата генерация транзакций")
    transactions = transactions_gen.generate_transactuins_list(TRANSACTION_COUNT, TRANSACTION_SIZE)
    for i in range(len(transactions)):
        signature = hashlib.sha256(transactions[i].encode("utf-8")).hexdigest()
        transactions[i] = (transactions[i], signature)
    print("Транзакции сформированы")
    network.send_message(client_socket, transactions)
    client_socket.close()
