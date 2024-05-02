import socket
import hashlib
import transactions_gen
import network
import paint
import json

from consolemenu import prompt_utils, ConsoleMenu, SelectionMenu, Screen
from consolemenu.items import FunctionItem
socket.setdefaulttimeout(2)
SERVER_ADDRESS = ('25.18.233.38',7001)
TRANSACTION_COUNT = 1000
TRANSACTION_SIZE = 1024

def send_message(sock:socket.socket):

    count = int(input("Введите количество транзакций\n>>> "))
    network.send_command(sock, "SERV")
    print("Начата генерация транзакций")
    transactions = transactions_gen.generate_transactuins_list(count, TRANSACTION_SIZE)
    for i in range(len(transactions)):
        signature = hashlib.sha256(transactions[i].encode("utf-8")).hexdigest()
        transactions[i] = (transactions[i], signature)
    print("Транзакции сформированы")
    notsend_prompt = prompt_utils.PromptUtils(Screen())
    network.send_message(sock, transactions)
    notsend_prompt.enter_to_continue()


def get_statistic(sock: socket.socket):
    count = int(input("Введите количество транзакций\n>>> "))
    network.send_command(sock, "STAT")
    sock.send(count.to_bytes(4, 'little'))
    stat = sock.recv(1024).decode("utf-8")
    with open("statistic.txt", "a") as f:
        f.write(stat + '\n')


def print_blockchain(sock: socket.socket):
    network.send_command(sock, "DRAW")
    data = network.receive_message(sock)
    paint.get_graph(data)


if __name__ == "__main__":
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(SERVER_ADDRESS)
    print("Клиент подключился к серверу ")
    # os.system('cls')
    menu = ConsoleMenu(f"CLIENT: {SERVER_ADDRESS[0]}:{SERVER_ADDRESS[1]}")
    item1 = FunctionItem("Отправить транзакции", send_message, [client_socket])
    item2 = FunctionItem("Посчитать статистику", get_statistic, [client_socket])
    item3 = FunctionItem("Вывести блокчейн", print_blockchain, [client_socket])
    menu.append_item(item1)
    menu.append_item(item2)
    menu.append_item(item3)
    menu.show()
    network.send_command(client_socket, "EXIT")
    client_socket.close()
