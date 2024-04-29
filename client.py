import socket
import hashlib
import transactions_gen
import network
import os

from consolemenu import prompt_utils, ConsoleMenu, SelectionMenu, Screen
from consolemenu.items import FunctionItem
socket.setdefaulttimeout(2)
SERVER_ADDRESS = ('25.18.233.38',7001)
TRANSACTION_COUNT = 1000
TRANSACTION_SIZE = 1024

    

if __name__ == "__main__":
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(SERVER_ADDRESS)
    print("Клиент подключился к серверу ")
    os.system('cls')
    while True:
        print("1. Отправить транзакции")
        print("2. Выход")
        choice = int(input(">>>  "))
        if choice == 1:
            size = int(input("Введите количество транзакций\n>>> "))
            print("Начата генерация транзакций")
            transactions = transactions_gen.generate_transactuins_list(TRANSACTION_COUNT, size)
            for i in range(len(transactions)):
                signature = hashlib.sha256(transactions[i].encode("utf-8")).hexdigest()
                transactions[i] = (transactions[i], signature)
            print("Транзакции сформированы")
            network.send_message(client_socket, transactions)
        if choice == 2:
            break
        os.system('cls')
    client_socket.close()
